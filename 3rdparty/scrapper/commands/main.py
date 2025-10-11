import Platform.StellarcatalogPlatformInstance as Instance


def main():
    scrapper = Instance.GetScrapperInstance()
    dataHolder = Instance.GetSolarSystemDataHolderInstance()

    if scrapper.scrap(dataHolder):
        dataHolder.saveToFile()


if __name__ == '__main__':
    main()
