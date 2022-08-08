# Resource Scrapper

## Data Format

* sources
    * (page number).json
        * source_db_id
        * source_id
        * title
        * icon
        * url
        * num_resources 
        * num_resource_pages 

* resources
    * source_id
        * (page number).json
            * resource_db_id
            * resource_id
            * title
            * url
            * authors
            * tags
            * publishedOn

## LOGGING Format

[INFO | ERROR]:[DATE TIME]:[SOURCE TITLE] [SOURCE | RESOURCE]:[ADD | UPDATE | DELETE] TITLE

# TODO

* Add github actions to run the scrappers scripts
    * Two different branches for hosting sqlite database, sources and resources directory
    * Checkout the main branch and copy the database (from db branch) and run the scrapper scripts and then save the db and updated sources, resources folder into data branch
    * Host the db with git large file storage

* Modify logging format

* Github Actions
    * On commit to main channel, create db and push to sources and resources
    * Postpone action to run after main action