import argparse

import Platform


def chcekGeneratorFlag() -> bool:
    parser = argparse.ArgumentParser(description="Scrapper runner")
    parser.add_argument(
        "-g", "--genData",
        action="store_true",
        help="Enable generate data mode"
    )
    args = parser.parse_args()
    return args.genData

def main():

    if chcekGeneratorFlag():
        print("Run scrapper in generate data mode.")
        platformInstance = Platform.loadPlatform("GereratorPlatformInstance")
    else:
        platformInstance = Platform.loadPlatform("StellarcatalogPlatformInstance")

    scrapper = platformInstance.GetScrapperInstance()
    dataHolder = platformInstance.GetSolarSystemDataHolderInstance()

    if scrapper.scrap(dataHolder):
        dataHolder.saveToFile()


if __name__ == '__main__':
    main()
