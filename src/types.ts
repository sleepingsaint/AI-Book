export type SourceType = {
    source_db_id: number;
    source_id: string;
    title: string;
    url: string;
    icon: string;
    num_resources: number;
    num_resource_pages: number;
};

export type ResourceType = {
    resource_db_id: number;
    resource_id: string;
    title: string;
    url: string;
    authors?: string;
    tags?: string;
    publishedOn?: string;
};