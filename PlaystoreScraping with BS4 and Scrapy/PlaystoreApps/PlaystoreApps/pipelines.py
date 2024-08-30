# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from PlaystoreApps.items import PlaystoreappsItem, OrganizationItem
import json
import os

class PlaystoreappsPipeline:
    def process_item(self, item, spider):
        return item
 


# class MultipleFilesPipeline:
#     def open_spider(self, spider):
#         # Create a directory to store outputs
#         self.query = getattr(spider, 'query', 'default')  # Access the query from the spider
#         self.output_dir = 'output_files'
#         os.makedirs(self.output_dir, exist_ok=True)

#         # Open files dynamically based on the query
#         self.file1 = open(f'{self.output_dir}/{self.query}_app_details.json', 'w', encoding='utf-8')
#         self.file2 = open(f'{self.output_dir}/{self.query}_organization.json', 'w', encoding='utf-8')

#     def close_spider(self, spider):
#         # Close the files when the spider closes
#         self.file1.close()
#         self.file2.close()

#     def process_item(self, item, spider):
#         # Write items to the correct file based on their type
#         if isinstance(item, PlaystoreappsItem):
#             line = json.dumps(dict(item), ensure_ascii=False) + "\n"
#             self.file1.write(line)
#         elif isinstance(item, OrganizationItem):
#             line = json.dumps(dict(item), ensure_ascii=False) + "\n"
#             self.file2.write(line)
#         return item
