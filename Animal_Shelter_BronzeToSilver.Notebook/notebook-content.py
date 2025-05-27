# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "80d50717-b435-4716-bae3-88c277739ab3",
# META       "default_lakehouse_name": "SilverLayer",
# META       "default_lakehouse_workspace_id": "fe1e2273-dd6c-49a9-bd71-3a813fd838bd",
# META       "known_lakehouses": [
# META         {
# META           "id": "80d50717-b435-4716-bae3-88c277739ab3"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import lit, col,isnull, count,desc, max
from pyspark.sql.types import StructType, StructField, IntegerType, TimestampType, StringType, DateType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

staff_Schema = StructType([StructField('Email', StringType(), True), StructField('Hire_Date', DateType(), True), StructField('IsActive', StringType(), False)])

animals_Schema = StructType([StructField('Name', StringType(), True), StructField('Species', StringType(), True), StructField('Primary_Color', StringType(), True), StructField('Implant_Chip_ID', StringType(), True), StructField('Breed', StringType(), True), StructField('Gender', StringType(), True), StructField('Birth_Date', DateType(), True), StructField('Pattern', StringType(), True), StructField('Admission_Date', DateType(), True)])

adoptions_Schema = StructType([StructField('Name', StringType(), True), StructField('Species', StringType(), True), StructField('Adopter_Email', StringType(), True), StructField('Adoption_Date', DateType(), True), StructField('Adoption_Fee', IntegerType(), True)])

persons_Schema = StructType([StructField('Email', StringType(), True), StructField('First_Name', StringType(), True), StructField('Last_Name', StringType(), True), StructField('Birth_Date', StringType(), True), StructField('Address', StringType(), True), StructField('State', StringType(), True), StructField('City', StringType(), True), StructField('Zip_Code', IntegerType(), True)])

vaccinations_Schema = StructType([StructField('Name', StringType(), True), StructField('Species', StringType(), True), StructField('Vaccination_Time', TimestampType(), True), StructField('Vaccine', StringType(), True), StructField('Batch', StringType(), True), StructField('Comments', StringType(), True), StructField('Email', StringType(), True)])

staff_assignments_Schema = StructType([StructField('Email', StringType(), True), StructField('Role', StringType(), True), StructField('Assigned', StringType(), True)])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

staff = spark.read.format('csv').schema(staff_Schema).load('abfss://Animal_Shelter@onelake.dfs.fabric.microsoft.com/BronzeLayer.Lakehouse/Files/Animal_Shelter_Staff.csv')
animals = spark.read.format('csv').schema(animals_Schema).load('abfss://Animal_Shelter@onelake.dfs.fabric.microsoft.com/BronzeLayer.Lakehouse/Files/Animal_Shelter_Animals.csv')
adoptions = spark.read.format('csv').schema(adoptions_Schema).load('abfss://Animal_Shelter@onelake.dfs.fabric.microsoft.com/BronzeLayer.Lakehouse/Files/Animal_Shelter_Adoptions.csv')
persons = spark.read.format('csv').schema(persons_Schema).load('abfss://Animal_Shelter@onelake.dfs.fabric.microsoft.com/BronzeLayer.Lakehouse/Files/Animal_Shelter_Persons.csv')
vaccinations = spark.read.format('csv').schema(vaccinations_Schema).load('abfss://Animal_Shelter@onelake.dfs.fabric.microsoft.com/BronzeLayer.Lakehouse/Files/Animal_Shelter_Vaccinations.csv')
staff_assignments = spark.read.format('csv').schema(staff_assignments_Schema).load('abfss://Animal_Shelter@onelake.dfs.fabric.microsoft.com/BronzeLayer.Lakehouse/Files/Animal_Shelter_Staff_Assignments.csv')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

staff.write.mode('overwrite').saveAsTable('staff')
animals.write.mode('overwrite').saveAsTable('animals')
adoptions.write.mode('overwrite').saveAsTable('adoptions')
persons.write.mode('overwrite').saveAsTable('persons')
vaccinations.write.mode('overwrite').saveAsTable('vaccinations')
staff_assignments.write.mode('overwrite').saveAsTable('staff_assignments')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
