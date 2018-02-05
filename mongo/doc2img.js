db.Corpus_Playground.aggregate(
    // Pipeline
    [
        // Stage 1
        {
            $match: {
                "findings.0": {$exists: true}
            }
        },

        // Stage 2
        {
            $project: {
                DOI: 1, journalName: 1, discipline: 1, authors: 1, title: 1, year: 1, findings: 1
            }
        },

        // Stage 3
        {
            $unwind: "$findings"
        },

        // Stage 4
        {
            $project: {
                _id: 0,
                URL: "$findings.URL2Image",
                ImageType: "$findings.v1_label",
                CaptionBody: "$findings.captionBody",
                CaptionTitle: "$findings.captionTitle",
                DOI: 1, journalName: 1, discipline: 1, authors: 1, title: 1, year: 1,
                Expanded: {
                    $map:
                        {
                            input: "$findings.acronym",
                            as: "acr",
                            in: {$arrayElemAt: ["$$acr", 1]}
                        }
                }
            }
        },

        // Stage 5
        {
            $out: "Images"
        },

    ]

    // Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
