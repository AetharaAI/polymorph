// ═══════════════════════════════════════════════════════════════
// AETHER-MAX MONGODB INIT SCRIPT
// Runs once on first container startup
// Creates DB, users, collections, and vector search indexes
// ═══════════════════════════════════════════════════════════════

// Switch to aether_memory database
db = db.getSiblingDB('aether_memory');

// ─────────────────────────────────────────────
// CREATE APPLICATION USER
// ─────────────────────────────────────────────
db.createUser({
  user: "aether_agent",
  pwd: "CHANGE_ME_AGENT_PASS",    // ← change before deploy
  roles: [
    { role: "readWrite", db: "aether_memory" },
    { role: "dbAdmin",   db: "aether_memory" }
  ]
});

// ─────────────────────────────────────────────
// COLLECTION: episodes
// Stores summarized past conversations with embeddings
// BGE embedding dim: 1024 (bge-large-en-v1.5) or 768 (bge-base)
// ─────────────────────────────────────────────
db.createCollection("episodes", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["agent_id", "session_id", "summary", "embedding", "created_at"],
      properties: {
        agent_id:    { bsonType: "string" },
        session_id:  { bsonType: "string" },
        user_id:     { bsonType: "string" },
        summary:     { bsonType: "string", description: "LLM-generated summary of the conversation" },
        raw_excerpt: { bsonType: "string", description: "Key raw messages, truncated" },
        embedding:   { bsonType: "array",  description: "BGE embedding of the summary" },
        tags:        { bsonType: "array",  description: "Auto-extracted topic tags" },
        tools_used:  { bsonType: "array",  description: "Tool names invoked in this session" },
        importance:  { bsonType: "double", description: "Importance score 0.0-1.0" },
        created_at:  { bsonType: "date" }
      }
    }
  }
});

// ─────────────────────────────────────────────
// COLLECTION: knowledge
// Semantic memory — distilled facts, entities, preferences
// ─────────────────────────────────────────────
db.createCollection("knowledge", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["agent_id", "entity", "fact", "embedding", "created_at"],
      properties: {
        agent_id:         { bsonType: "string" },
        entity:           { bsonType: "string", description: "What this fact is about" },
        fact:             { bsonType: "string", description: "The distilled fact/knowledge" },
        embedding:        { bsonType: "array" },
        confidence:       { bsonType: "double", description: "0.0-1.0" },
        source_episodes:  { bsonType: "array",  description: "Episode _ids this was derived from" },
        category:         { bsonType: "string", description: "entity | preference | domain | project | person" },
        created_at:       { bsonType: "date" },
        updated_at:       { bsonType: "date" }
      }
    }
  }
});

// ─────────────────────────────────────────────
// COLLECTION: procedures
// Learned tool patterns and playbooks
// ─────────────────────────────────────────────
db.createCollection("procedures", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["agent_id", "task_type", "description", "steps", "embedding", "created_at"],
      properties: {
        agent_id:       { bsonType: "string" },
        task_type:      { bsonType: "string" },
        description:    { bsonType: "string", description: "What this procedure accomplishes" },
        steps:          { bsonType: "array",  description: "Ordered list of tool calls and logic" },
        tools_sequence: { bsonType: "array",  description: "Just the tool names in order" },
        embedding:      { bsonType: "array",  description: "BGE embedding of description" },
        success_count:  { bsonType: "int" },
        avg_iterations: { bsonType: "double" },
        example_session:{ bsonType: "string", description: "session_id of canonical example" },
        created_at:     { bsonType: "date" },
        updated_at:     { bsonType: "date" }
      }
    }
  }
});

// ─────────────────────────────────────────────
// REGULAR INDEXES
// ─────────────────────────────────────────────
db.episodes.createIndex({ agent_id: 1 });
db.episodes.createIndex({ session_id: 1 }, { unique: true });
db.episodes.createIndex({ created_at: -1 });
db.episodes.createIndex({ tags: 1 });
db.episodes.createIndex({ importance: -1 });
db.episodes.createIndex({ agent_id: 1, created_at: -1 });

db.knowledge.createIndex({ agent_id: 1 });
db.knowledge.createIndex({ entity: 1 });
db.knowledge.createIndex({ category: 1 });
db.knowledge.createIndex({ agent_id: 1, entity: 1 });
db.knowledge.createIndex({ updated_at: -1 });

db.procedures.createIndex({ agent_id: 1 });
db.procedures.createIndex({ task_type: 1 });
db.procedures.createIndex({ success_count: -1 });
db.procedures.createIndex({ agent_id: 1, task_type: 1 });

// ─────────────────────────────────────────────
// VECTOR SEARCH INDEXES
// NOTE: MongoDB Atlas has native $vectorSearch
// For self-hosted Mongo 7, we use a manual approach:
// Store embeddings in docs + use cosine similarity in aggregation
// OR upgrade to Atlas / use the community vector search plugin
//
// The backend memory service will handle vector search via:
// Option A: MongoDB aggregation with $dotProduct (approximate)
// Option B: Pre-filter with metadata, then cosine similarity in Python
// Option C: Keep Qdrant for pure vector search, MongoDB for docs
//           (recommended if you want <10ms retrieval)
//
// See VECTOR_SEARCH_NOTE.md for implementation details
// ─────────────────────────────────────────────

// ─────────────────────────────────────────────
// SEED: Initial knowledge about Cory / AetherPro
// ─────────────────────────────────────────────
const seedDate = new Date();

db.knowledge.insertMany([
  {
    agent_id: "aether-max",
    entity: "AetherPro Technologies",
    fact: "AI infrastructure company founded by Cory in May 2024. Focuses on sovereign, self-hosted AI systems. SAM.gov registered, CAGE code 174V7.",
    embedding: [],   // will be populated by the memory service on first embed pass
    confidence: 1.0,
    source_episodes: [],
    category: "project",
    created_at: seedDate,
    updated_at: seedDate
  },
  {
    agent_id: "aether-max",
    entity: "RedWatch",
    fact: "Cybersecurity platform for US defense contractors. Implements MITRE ATT&CK matrices and CMMC 2.0 compliance controls. Primary federal contract target.",
    embedding: [],
    confidence: 1.0,
    source_episodes: [],
    category: "project",
    created_at: seedDate,
    updated_at: seedDate
  },
  {
    agent_id: "aether-max",
    entity: "Infrastructure",
    fact: "OVHcloud Scale tier ($10K/mo credits), L40S GPU instances. Services: Redis Stack, PostgreSQL, MongoDB x2, Qdrant, NATS x3, BGE embedding model, BGE reranker model, OpenTelemetry.",
    embedding: [],
    confidence: 1.0,
    source_episodes: [],
    category: "domain",
    created_at: seedDate,
    updated_at: seedDate
  },
  {
    agent_id: "aether-max",
    entity: "Cory",
    fact: "Licensed master electrician 15+ years commercial experience. Self-taught AI developer since April 2024. Direct communication style. First-principles problem solver. Minimal sleep, high output.",
    embedding: [],
    confidence: 1.0,
    source_episodes: [],
    category: "person",
    created_at: seedDate,
    updated_at: seedDate
  }
]);

print("✅ aether_memory database initialized");
print("✅ Collections: episodes, knowledge, procedures");
print("✅ Indexes created");
print("✅ Seed knowledge inserted");
print("⚠️  Change passwords before production!");
print("⚠️  Populate embeddings via: python memory_service/embed_seed.py");
