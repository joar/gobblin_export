# A tool to download your media from gobblin.se

## Installation 

To install, run:

    git clone https://github.com/joar/gobblin_export.git
    cd gobblin_export
    pip install -r requirements.txt  # Might want to use a virtualenv
     
## Usage

Run 
    # When in the directory of the scrapy.cfg file
    scrapy crawl gobblin -a username=joar
    
and your files will end up in a folder named `downloaded`.
    
 