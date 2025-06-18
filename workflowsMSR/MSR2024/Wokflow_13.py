from newDSL.metadata.Metadata import Metadata
from newDSL.operator.OperatorFactory import OperatorFactory
from newDSL.element.loader.LoaderFactory import LoaderFactory
from newDSL.element.writer.WritterFactory import WritterFactory

# DATAR: A Dataset for Tracking App Releases
# DOI : 10.1145/3643991.3644892

# *Filter repos with 'Android' topic
# *Filter repos created after end of Novembert 2023
# *Exclude repos without AndroidManifest.xml file in the default branch


filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    # What about the steps about the package name ?

    topic = Metadata.of_string("topic")
    creation_date = Metadata.of_string("creationDate")
    hasAndroidManifest = Metadata.of_boolean("hasAndroidManifest")

    op = (
        filter_operator(topic.bool_constraint(lambda x: x == "Android"))
        .chain(filter_operator(creation_date.bool_constraint(lambda x: x >= "2023-12-01")))
        .chain(filter_operator(hasAndroidManifest.bool_constraint(lambda x: x)))
        .input(json_loader("input.json", topic, creation_date, hasAndroidManifest))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)