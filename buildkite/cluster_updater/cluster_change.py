import requests
import os

API_BASE_URL = "https://api.buildkite.com/v2"

API_TOKEN = os.environ.get("BUILDKITE_API_TOKEN")

ORG_SLUG = "ORG_SLUG_HERE"

NEW_CLUSTER_ID = "CLUSTER_ID_HERE"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_pipelines(page=1):
    """Fetch pipelines with pagination"""
    url = f"{API_BASE_URL}/organizations/{ORG_SLUG}/pipelines"
    params = {"page": page, "per_page": 100}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def update_pipeline(pipeline_slug, new_cluster):
    """Update pipeline with new cluster"""
    url = f"{API_BASE_URL}/organizations/{ORG_SLUG}/pipelines/{pipeline_slug}"
    data = {"cluster_id": new_cluster}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def confirm_update(pipeline_slug, current_cluster):
    """Ask for user confirmation before updating a pipeline"""
    while True:
        response = input(f"Update pipeline '{pipeline_slug}' (current cluster: {current_cluster}) to new cluster '{NEW_CLUSTER_ID}'? (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' for yes or 'n' for no.")

def main():
    page = 1
    while True:
        pipelines = get_pipelines(page)
        if not pipelines:
            break

        for pipeline in pipelines:
            print(f"\nPipeline: {pipeline['slug']}")
            current_cluster = pipeline.get('cluster_id')
            if current_cluster == NEW_CLUSTER_ID:
                print(f"\nSkipping pipeline '{pipeline['name']}' - already on cluster '{current_cluster}'")
                continue
            if confirm_update(pipeline['slug'], current_cluster):
                updated_pipeline = update_pipeline(pipeline['slug'], NEW_CLUSTER_ID)
                print(f"Updated pipeline: {updated_pipeline['slug']} to cluster: {updated_pipeline['cluster_id']}")
            else:
                print(f"Skipped pipeline: {pipeline['slug']}")

        page += 1

if __name__ == "__main__":
    main()
