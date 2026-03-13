# VECTOR SEARCH ARCHITECTURE NOTE
# Aether-Max Memory Layer

## The Self-Hosted MongoDB Vector Search Problem

MongoDB Atlas has native `$vectorSearch` with HNSW indexing.
Self-hosted MongoDB 7 Community does NOT have this natively.

You have 3 options ranked by recommendation for your stack:

───────────────────────────────────────────────────────────────
## OPTION A: Hybrid — MongoDB docs + Qdrant for vectors (RECOMMENDED)
───────────────────────────────────────────────────────────────

You already have Qdrant running on this node. Use it.

  MongoDB stores:  Full documents (summary, metadata, tags, raw text)
  Qdrant stores:   Vectors + MongoDB _id as payload

  FLOW:
    Write:  embed text → store vector in Qdrant (with mongo_id payload)
            → store full doc in MongoDB

    Read:   embed query → Qdrant similarity search → get mongo_ids
            → BGE reranker on top-20 candidates
            → fetch full docs from MongoDB by _id
            → return top-5 to agent

  PROS: Fastest possible retrieval, HNSW index, <5ms vector search
  CONS: Two services to keep in sync (mitigated by atomic write logic)

  Collections map to Qdrant:
    MongoDB episodes   → Qdrant collection: aether_episodes
    MongoDB knowledge  → Qdrant collection: aether_knowledge
    MongoDB procedures → Qdrant collection: aether_procedures

───────────────────────────────────────────────────────────────
## OPTION B: Pure MongoDB with aggregation pipeline
───────────────────────────────────────────────────────────────

Use MongoDB's $function or Python-side cosine similarity.
Works but is O(n) — fine up to ~10K docs, degrades after.

  db.episodes.aggregate([
    { $match: { agent_id: "aether-max" } },
    { $addFields: {
        score: {
          $reduce: {
            input: { $zip: { inputs: ["$embedding", query_vector] } },
            initialValue: 0,
            in: { $add: ["$$value", { $multiply: [
              { $arrayElemAt: ["$$this", 0] },
              { $arrayElemAt: ["$$this", 1] }
            ]}]}
          }
        }
    }},
    { $sort: { score: -1 } },
    { $limit: 20 }
  ])

  PROS: No extra service, simple
  CONS: Full collection scan, slow at scale, no HNSW

───────────────────────────────────────────────────────────────
## OPTION C: MongoDB Atlas (upgrade path)
───────────────────────────────────────────────────────────────

If you ever move to Atlas, just replace the vector search calls
with $vectorSearch pipeline stage. Zero code change to documents.

───────────────────────────────────────────────────────────────
## DECISION FOR AETHER-MAX

Go with OPTION A.

You already have Qdrant. Using it for vectors is the right call.
MongoDB handles the rich documents. Qdrant handles the ANN search.
BGE reranker sits between Qdrant results and the agent.

This is the same pattern used by production memory systems
like Mem0 and production RAG pipelines at scale.

Qdrant collections to create:
  - aether_episodes    (vectors: BGE 1024-dim or 768-dim)
  - aether_knowledge   (same dim)
  - aether_procedures  (same dim)

BGE embedding model output dimensions:
  - bge-large-en-v1.5:  1024
  - bge-base-en-v1.5:   768
  - bge-m3:             1024 (multilingual, better for diverse content)

Use whichever you have deployed. Match the dim in Qdrant collection config.
