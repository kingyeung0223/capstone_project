# capstone_project
My final year project which targets crawling real estate data from different websites and build a visualization platform.
To collect necessary data for building visualization platform, scrapy is used to crawl real-estate data online. Google API is also used to search for facilities surrounding every real estate. Eventually, all transformed data are fed into qliksense for visualization.

The folder "capstone_crawl" is a scrapy project used to crawl real-estate data online.
Inside "capstone_crawl", the folder "spiders" contains "scrapy_crawl.py" which define a scrapy spider object used to crawl real estate data.

"items.py" defines the item class which used as a real-estate data container.
"pipelines.py" defines necessary transformation or data-cleaning processes before saving the real-estate data into a csv.
"settings.py" defines feature of the scrapy spider.


Inside "capstone_crawl", the folder "data_processing" contains 3 python files: "google_estate_coor.py", "google_facilities.py", "retrieve_from_raw.py".

"retrieve_from_raw.py" is used to extract addresses of real-estates collected by scrapy spider. This is because the obtained csv is too large for processing in excel.

Extracted addresses are then used in "google_estate_coor.py". With google api, the address are transformed into geographical coordinates.

"google_facilities.py" used the extracted addresses together with google api to search for facilities surrounding every real-estate. The results are then exported as a csv file.


The pdf file describe the outputs and findings of building the visualization platform.
The mp4 file is a demonstration of using the visualization dashboard.
The qfv file is the qliksense dasboard.
