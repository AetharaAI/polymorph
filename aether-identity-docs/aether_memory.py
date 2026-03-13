"""
Aether Agentic Memory System
============================
Redis Stack-powered memory with TimeSeries, Search, JSON, Bloom Filters.

Layers:
  1. Daily Logs     (aether:daily:*)      — Raw event stream (HASH)
  2. Long-term      (aether:longterm:*)    — Promoted/compressed entries (HASH)
  3. Scratchpad     (aether:scratchpad:*)  — Active working memory (JSON)
  4. Notebook       (aether:notebook:*)    — Persistent knowledge (JSON)
  5. Checkpoints    (aether:checkpoint:*)  — Full snapshots (STRING/JSON)
  6. Episodes       (aether:episode:*)     — Compressed context (HASH/STRING)
  7. TimeSeries     (aether:ts:*)          — Numeric metrics over time
  8. Bloom Filters  (aether:bf:*)          — Probabilistic dedup

Usage:
  from aether_memory import AetherMemory
  mem = AetherMemory()
  mem.recover_context()  # After compression/checkpoint
  mem.write_scratchpad("task_name", {...})
  mem.search("redis setup", limit=5)
  mem.add_notebook("Title", "Content", category="architecture")
"""

import redis
import json
import hashlib
import datetime
import uuid
import time
from typing import Optional, List, Dict, Any, Tuple


class AetherMemory:
    """Comprehensive agentic memory backed by Redis Stack."""

    def __init__(self, host='redis-stack', port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        self._verify_connection()

    def _verify_connection(self):
        assert self.r.ping(), "Redis not reachable"

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    # ─── SCRATCHPAD (Working Memory) ─────────────────────────────

    def write_scratchpad(self, name: str, data: dict) -> str:
        """Write/update a scratchpad entry (active working memory)."""
        key = f"aether:scratchpad:{name}"
        data.setdefault('created_at', self._now())
        data['updated_at'] = self._now()
        data.setdefault('status', 'active')
        data.setdefault('priority', 5)
        self.r.execute_command('JSON.SET', key, '$', json.dumps(data))
        return key

    def read_scratchpad(self, name: str = 'current_task') -> Optional[dict]:
        """Read a scratchpad entry."""
        key = f"aether:scratchpad:{name}"
        try:
            val = self.r.execute_command('JSON.GET', key)
            return json.loads(val) if val else None
        except:
            return None

    def update_scratchpad(self, name: str, path: str, value: Any):
        """Update a specific field in a scratchpad entry."""
        key = f"aether:scratchpad:{name}"
        self.r.execute_command('JSON.SET', key, f'$.{path}', json.dumps(value))
        self.r.execute_command('JSON.SET', key, '$.updated_at', json.dumps(self._now()))

    def list_scratchpads(self) -> List[str]:
        """List all scratchpad entries."""
        keys = self.r.keys('aether:scratchpad:*')
        return [k.replace('aether:scratchpad:', '') for k in keys]

    def clear_scratchpad(self, name: str):
        """Remove a scratchpad entry."""
        self.r.delete(f"aether:scratchpad:{name}")

    # ─── NOTEBOOK (Persistent Knowledge) ─────────────────────────

    def add_notebook(self, title: str, content: str, category: str = 'general',
                     tags: List[str] = None, importance: int = 5,
                     summary: str = None) -> str:
        """Add a notebook entry (persistent knowledge)."""
        slug = title.lower().replace(' ', '_').replace('-', '_')[:50]
        key = f"aether:notebook:{slug}"
        entry = {
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "created_at": self._now(),
            "updated_at": self._now(),
            "importance": importance,
            "status": "active",
            "related_sessions": [],
            "summary": summary or content[:200]
        }
        self.r.execute_command('JSON.SET', key, '$', json.dumps(entry))
        return key

    def read_notebook(self, slug: str) -> Optional[dict]:
        """Read a notebook entry by slug."""
        key = f"aether:notebook:{slug}"
        try:
            val = self.r.execute_command('JSON.GET', key)
            return json.loads(val) if val else None
        except:
            return None

    def search_notebook(self, query: str, limit: int = 5) -> List[dict]:
        """Search the notebook index."""
        return self._ft_search('aether:notebook:idx', query, limit)

    # ─── SEARCH (Unified) ────────────────────────────────────────

    def search(self, query: str, limit: int = 10, index: str = None) -> List[dict]:
        """Search across memory. Default searches daily/longterm logs."""
        idx = index or 'aether:memory:idx'
        return self._ft_search(idx, query, limit)

    def search_all(self, query: str, limit: int = 5) -> Dict[str, List[dict]]:
        """Search across ALL indexes and return combined results."""
        results = {}
        for idx_name in ['aether:memory:idx', 'aether:notebook:idx',
                         'aether:scratchpad:idx', 'aether:episodes:idx',
                         'aether:checkpoints:idx']:
            try:
                hits = self._ft_search(idx_name, query, limit)
                if hits:
                    results[idx_name] = hits
            except:
                pass
        return results

    def _ft_search(self, index: str, query: str, limit: int = 10) -> List[dict]:
        """Execute an FT.SEARCH query."""
        try:
            # Escape special RediSearch characters in the query
            safe_query = query
            for char in ['@', '!', '{', '}', '(', ')', '|', '-', '~', '[', ']', '^']:
                safe_query = safe_query.replace(char, f'\\{char}')
            
            result = self.r.execute_command(
                'FT.SEARCH', index, safe_query,
                'LIMIT', '0', str(limit)
            )
            return self._parse_search_results(result)
        except Exception as e:
            # Fallback: try as-is
            try:
                result = self.r.execute_command(
                    'FT.SEARCH', index, query,
                    'LIMIT', '0', str(limit)
                )
                return self._parse_search_results(result)
            except:
                return []

    def _parse_search_results(self, result) -> List[dict]:
        """Parse FT.SEARCH results into list of dicts."""
        if not result or result[0] == 0:
            return []
        
        hits = []
        i = 1
        while i < len(result):
            key = result[i]
            i += 1
            if i < len(result) and isinstance(result[i], list):
                fields = result[i]
                doc = {'_key': key}
                for j in range(0, len(fields), 2):
                    field_name = fields[j]
                    field_val = fields[j + 1]
                    # Try to parse JSON values
                    if field_val and field_val.startswith('{'):
                        try:
                            field_val = json.loads(field_val)
                        except:
                            pass
                    doc[field_name] = field_val
                hits.append(doc)
                i += 1
            else:
                hits.append({'_key': key})
        return hits

    # ─── TIMESERIES ──────────────────────────────────────────────

    def ts_add(self, metric: str, value: float, timestamp: int = None):
        """Add a TimeSeries data point. metric is the suffix after aether:ts:"""
        key = f"aether:ts:{metric}"
        ts = timestamp or self._now_ms()
        self.r.execute_command('TS.ADD', key, ts, value)

    def ts_get(self, metric: str) -> Optional[Tuple[int, float]]:
        """Get latest TimeSeries value."""
        try:
            result = self.r.execute_command('TS.GET', f'aether:ts:{metric}')
            return result  # (timestamp, value)
        except:
            return None

    def ts_range(self, metric: str, from_ms: int = None, to_ms: int = None,
                 count: int = 100) -> List[Tuple[int, float]]:
        """Get TimeSeries range."""
        key = f"aether:ts:{metric}"
        from_ms = from_ms or '-'
        to_ms = to_ms or '+'
        try:
            return self.r.execute_command('TS.RANGE', key, from_ms, to_ms, 'COUNT', count)
        except:
            return []

    def record_memory_pressure(self, pressure: float):
        """Record current memory pressure (0.0-1.0)."""
        self.ts_add('memory:pressure', pressure)

    def record_checkpoint_event(self):
        """Record that a checkpoint was created."""
        self.ts_add('events:checkpoint', 1)

    def record_compression_event(self):
        """Record that context was compressed."""
        self.ts_add('events:compression', 1)

    def record_tool_call(self):
        """Record a tool call."""
        self.ts_add('tools:calls', 1)

    def record_search_quality(self, quality: float):
        """Record search result quality (0.0-1.0)."""
        self.ts_add('search:quality', quality)

    # ─── BLOOM FILTERS ───────────────────────────────────────────

    def is_content_seen(self, content: str) -> bool:
        """Check if content has been seen before (dedup)."""
        h = hashlib.md5(content.encode()).hexdigest()
        return bool(self.r.execute_command('BF.EXISTS', 'aether:bf:seen_content', h))

    def mark_content_seen(self, content: str):
        """Mark content as seen."""
        h = hashlib.md5(content.encode()).hexdigest()
        self.r.execute_command('BF.ADD', 'aether:bf:seen_content', h)

    def is_entity_known(self, entity: str) -> bool:
        """Check if an entity has been encountered before."""
        return bool(self.r.execute_command('BF.EXISTS', 'aether:bf:known_entities', entity))

    def register_entity(self, entity: str):
        """Register a new entity."""
        self.r.execute_command('BF.ADD', 'aether:bf:known_entities', entity)

    # ─── CONTEXT RECOVERY ────────────────────────────────────────

    def recover_context(self, verbose: bool = True) -> dict:
        """
        Full context recovery protocol. Call this after compression,
        checkpoint_and_continue, or any context loss event.
        
        Returns a dict with all recovered context.
        """
        context = {}

        # Step 1: What was I doing?
        scratchpad = self.read_scratchpad('current_task')
        if scratchpad:
            context['current_task'] = scratchpad
            if verbose:
                print(f"📋 CURRENT TASK: {scratchpad.get('task', 'unknown')}")
                print(f"   Status: {scratchpad.get('status', 'unknown')}")
                if scratchpad.get('key_facts'):
                    print(f"   Key facts: {len(scratchpad['key_facts'])}")
                    for fact in scratchpad['key_facts'][:5]:
                        print(f"     • {fact}")

        # Step 2: System state
        sys_state = self.read_scratchpad('system_state')
        if sys_state:
            context['system_state'] = sys_state

        # Step 3: Recent memory entries
        recent = self.search('*', limit=10)
        context['recent_entries'] = recent
        if verbose and recent:
            print(f"\n📝 RECENT MEMORY ({len(recent)} entries):")
            for entry in recent[:5]:
                content = entry.get('content', '')[:100]
                print(f"   [{entry.get('source', '?')}] {content}")

        # Step 4: TimeSeries state
        ts_state = {}
        for metric in ['memory:pressure', 'memory:tokens', 'session:activity']:
            val = self.ts_get(metric)
            if val:
                ts_state[metric] = val
        context['timeseries'] = ts_state
        if verbose and ts_state:
            print(f"\n📊 TIMESERIES:")
            for k, v in ts_state.items():
                print(f"   {k}: {v}")

        # Step 5: Active scratchpads
        pads = self.list_scratchpads()
        context['active_scratchpads'] = pads
        if verbose:
            print(f"\n🗒️  ACTIVE SCRATCHPADS: {pads}")

        # Step 6: Notebook knowledge count
        try:
            nb_result = self.r.execute_command('FT.SEARCH', 'aether:notebook:idx', '*', 'LIMIT', '0', '0')
            nb_count = nb_result[0] if nb_result else 0
            context['notebook_entries'] = nb_count
            if verbose:
                print(f"📓 NOTEBOOK ENTRIES: {nb_count}")
        except:
            pass

        return context

    def quick_orient(self) -> str:
        """Quick one-line orientation after context loss."""
        task = self.read_scratchpad('current_task')
        if task:
            return f"Task: {task.get('task', '?')} | Status: {task.get('status', '?')} | Priority: {task.get('priority', '?')}"
        return "No active task in scratchpad."

    # ─── DAILY LOG HELPERS ───────────────────────────────────────

    def log(self, content: str, source: str = 'agent', tags: str = '',
            score: float = 1.0, importance: int = 5) -> str:
        """Write a daily log entry."""
        today = datetime.date.today().isoformat()
        entry_id = uuid.uuid4().hex[:8]
        key = f"aether:daily:{today}:{entry_id}"
        
        # Dedup check
        if self.is_content_seen(content):
            return f"DEDUP:{key}"
        
        self.r.hset(key, mapping={
            'content': content,
            'source': source,
            'tags': tags,
            'score': score,
            'timestamp': self._now(),
            'importance': importance,
            'type': source
        })
        self.mark_content_seen(content)
        return key

    # ─── CHECKPOINT METADATA ─────────────────────────────────────

    def index_checkpoint(self, checkpoint_key: str, name: str = None,
                         summary: str = None, tags: List[str] = None):
        """Create searchable metadata for a checkpoint."""
        try:
            val = self.r.get(checkpoint_key)
            if not val:
                return
            data = json.loads(val)
            cp_uuid = data.get('uuid', checkpoint_key.split(':')[-1])
            
            meta = {
                "name": name or data.get('name', 'unnamed'),
                "summary": summary or f"Checkpoint with {len(data.get('daily', {}))} entries",
                "timestamp": data.get('timestamp', self._now()),
                "session_id": "unknown",
                "tags": tags or ["checkpoint"],
                "key_entities": [],
                "task_context": "",
                "original_key": checkpoint_key,
                "uuid": cp_uuid
            }
            
            meta_key = f"aether:cp:{cp_uuid}"
            self.r.execute_command('JSON.SET', meta_key, '$', json.dumps(meta))
            return meta_key
        except Exception as e:
            return None

    # ─── STATS ───────────────────────────────────────────────────

    def stats(self) -> dict:
        """Get comprehensive memory statistics."""
        stats = {}
        
        # Key counts by pattern
        for pattern, label in [
            ('aether:daily:*', 'daily_logs'),
            ('aether:longterm:*', 'longterm'),
            ('aether:scratchpad:*', 'scratchpads'),
            ('aether:notebook:*', 'notebook'),
            ('aether:checkpoint:*', 'checkpoints'),
            ('aether:episode:*', 'episodes'),
            ('aether:ts:*', 'timeseries'),
            ('aether:bf:*', 'bloom_filters'),
            ('aether:cp:*', 'checkpoint_meta'),
        ]:
            stats[label] = len(self.r.keys(pattern))
        
        # Index doc counts
        for idx in ['aether:memory:idx', 'aether:notebook:idx', 'aether:scratchpad:idx',
                     'aether:episodes:idx', 'aether:checkpoints:idx']:
            try:
                info = self.r.execute_command('FT.INFO', idx)
                info_dict = dict(zip(info[::2], info[1::2]))
                label = idx.split(':')[1]  # memory, notebook, scratchpad, episodes, checkpoints
                stats[f'idx_{label}'] = int(info_dict.get('num_docs', 0))
            except:
                label = idx.split(':')[1]
                stats[f'idx_{label}'] = 'N/A'
        
        stats['total_keys'] = len(self.r.keys('aether:*'))
        return stats

    def print_stats(self):
        """Print formatted memory statistics."""
        s = self.stats()
        print("═" * 50)
        print("  AETHER MEMORY STATISTICS")
        print("═" * 50)
        print(f"  Total keys:        {s['total_keys']}")
        print(f"  Daily logs:        {s['daily_logs']}")
        print(f"  Long-term:         {s['longterm']}")
        print(f"  Scratchpads:       {s['scratchpads']}")
        print(f"  Notebook entries:  {s['notebook']}")
        print(f"  Checkpoints:       {s['checkpoints']}")
        print(f"  Episodes:          {s['episodes']}")
        print(f"  TimeSeries:        {s['timeseries']}")
        print(f"  Bloom Filters:     {s['bloom_filters']}")
        print(f"  Checkpoint Meta:   {s['checkpoint_meta']}")
        print(f"  ─────────────────────────────────")
        print(f"  Index docs (memory):      {s.get('idx_memory', 'N/A')}")
        print(f"  Index docs (notebook):    {s.get('idx_notebook', 'N/A')}")
        print(f"  Index docs (scratchpad):  {s.get('idx_scratchpad', 'N/A')}")
        print(f"  Index docs (episodes):    {s.get('idx_episodes', 'N/A')}")
        print(f"  Index docs (checkpoints): {s.get('idx_checkpoints', 'N/A')}")
        print("═" * 50)


# ─── CONVENIENCE FUNCTIONS ───────────────────────────────────────

def connect(host='redis-stack', port=6379) -> AetherMemory:
    """Quick connect."""
    return AetherMemory(host=host, port=port)

def recover():
    """Quick context recovery."""
    mem = AetherMemory()
    return mem.recover_context()

def orient():
    """Quick orientation."""
    mem = AetherMemory()
    return mem.quick_orient()

def stats():
    """Quick stats."""
    mem = AetherMemory()
    mem.print_stats()


if __name__ == '__main__':
    print("Aether Memory System — Self Test\n")
    mem = AetherMemory()
    
    # Stats
    mem.print_stats()
    
    # Context recovery
    print("\n")
    ctx = mem.recover_context()
    
    # Search test
    print("\n🔍 Search test: 'redis'")
    results = mem.search_all('redis', limit=3)
    for idx_name, hits in results.items():
        print(f"\n  {idx_name}:")
        for hit in hits:
            content = str(hit.get('content', hit.get('title', hit.get('task', '?'))))[:80]
            print(f"    → {content}")
    
    print("\n✅ Self-test complete!")
