import pandas as pd
import wikipedia
from mongoDBOperations import MongoDBManagement

from PIL import Image
import io



class wikiScrapper:

    def __init__(self, searchString):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        self.searchString = searchString


    def WikiSummary(self):
        """
        This function helps to get summary
        """
        try:
            result = wikipedia.summary(self.searchString, sentences=3)
            return result
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(Summary) - Disambiguation Error for the term {self.searchString}. Please try other id")

    def WikiReference(self):
        """
        This function helps to save references
        """
        try:
            et_page = wikipedia.page(self.searchString)
            refs = et_page.references
            #refs_df = pd.DataFrame(refs, index = None, columns = ['References'])
            return refs
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(Wikireference) - Something went wrong while saving references. \n" + str(e))

    def WikiImages(self):
        """
        This function helps to save images
        """
        try:
            et_page = wikipedia.page(self.searchString)
            images = et_page.images
            #refs_df = pd.DataFrame(refs, index = None, columns = ['References'])
            return images
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(WikiImages) - Something went wrong while saving images. \n" + str(e))


    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def getSummaryToDisplay(self,username, password):
        """
        This function returns the summary and other detials of product
        """
        try:
            search = self.searchString
            mongoClient = MongoDBManagement(username=username, password=password)
            summary = self.WikiSummary()
            references = self.WikiReference()
            images = self.WikiImages()
            #https://stackoverflow.com/questions/47668507/how-to-store-images-in-mongodb-through-pymongo/47669016
            result = {'summary': summary, 'reference': references, 'images': images}
            mongoClient.insertImages(db_name="Wikipedia-Scrapper_Images",
                                     collection_name=search + "_images",
                                     images=images)
            mongoClient.insertRecord(db_name="Wikipedia-Scrapper",
                                     collection_name= search,
                                     record=result)
            return result
        except Exception as e:
            raise Exception(f"(Summary) - Something went wrong" + str(e))
