import handlePub,handleFellow

fileNames=["paperLXD.bib"]
for file in fileNames:
    handlePub.parse_bibtex(file)
    # handleFellow.check_fellow_by_names(handleFellow.list_authors(file), file)
