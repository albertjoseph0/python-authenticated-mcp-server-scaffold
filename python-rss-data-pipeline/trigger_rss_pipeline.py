import modal

trigger_rss_pipeline = modal.Function.from_name("rss-to-vector-pipeline", "rss_to_vector_job")

trigger_rss_pipeline.remote()