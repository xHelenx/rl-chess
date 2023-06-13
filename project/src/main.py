
from SampleConverter import SampleConverter
from constants import PATH, FILE
if __name__ == "__main__":
    sampleConv = SampleConverter()
    sampleConv.read_dataset(PATH + FILE )
    