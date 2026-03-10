prepare_obi_data.py is used to transform raw data provided by OBI into SCAFFOLD's required data ingestion model

analysis.py is used to calculate count of measures used to create a candidate each month and number of months messages are generated for each subject

filter_comparator_measure_report.py is used to clean up comparator file removing data for some of the measures

duplicate_rows_comparator_measure_report.py is used to add goal comparator for some of the measures which have not had them added before.