# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f5fac1a5-b55c-479f-a7fa-3d6ff0f87d4c",
# META       "default_lakehouse_name": "GoldLayer",
# META       "default_lakehouse_workspace_id": "fe1e2273-dd6c-49a9-bd71-3a813fd838bd",
# META       "known_lakehouses": [
# META         {
# META           "id": "f5fac1a5-b55c-479f-a7fa-3d6ff0f87d4c"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from delta.tables import DeltaTable
from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

animal = DeltaTable.forName(spark, "SilverLayer.animals")
staff = DeltaTable.forName(spark, "SilverLayer.staff")
person = DeltaTable.forName(spark, "SilverLayer.persons")
staff_asig = DeltaTable.forName(spark, "SilverLayer.staff_assignments")
adopter = DeltaTable.forName(spark, "SilverLayer.adoptions")
vaccine = DeltaTable.forName(spark, "SilverLayer.vaccinations")

df_animal = animal.toDF()
df_staff = staff.toDF()
df_person = person.toDF()
df_staff_asig = staff_asig.toDF()
df_adopter = adopter.toDF()
df_vaccine = vaccine.toDF()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

window_Animal = Window.orderBy('Name', 'Species')
df_animal = df_animal.withColumn('Animal_Id', row_number().over(window_Animal)).select('Animal_Id','Name', 'Species', 'Primary_Color', 'Breed', 'Gender', 'Birth_Date', 'Pattern') 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

window_Staff = Window.orderBy('Email')
df_staff = df_staff.withColumn('Staff_Id', row_number().over(window_Staff)).join(df_person, df_staff.Email == df_person.Email, "inner")\
            .join(df_staff_asig, df_staff.Email == df_staff_asig.Email )\
            .select("Staff_Id", "First_Name", "Last_Name","Birth_Date", "State", "City", "Zip_Code", "Role", df_person.Email)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_staff)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_adopter)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

Window_Adopter = Window.orderBy('Adopter_Email')
df_adopter = df_adopter.select('Adopter_Email').distinct()
df_adopter = df_adopter.withColumn('Adopter_Id', row_number().over(Window_Adopter)).join(df_person, df_adopter.Adopter_Email == df_person.Email, "inner")\
                .withColumnRenamed('First_Name', 'Adopter_First_Name')\
                .withColumnRenamed('Last_Name', 'Adopter_Last_Name')\
                .withColumnRenamed('Birth_Date', 'Adopter_Birth_Date')\
                .withColumnRenamed('State', 'Adopter_State')\
                .withColumnRenamed('City', 'Adopter_City')\
                .select('Adopter_Id', 'Adopter_First_Name', 'Adopter_Last_Name', 'Adopter_Email', 'Adopter_Birth_Date', 'Adopter_State', 'Adopter_City' )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_adopter)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

Window_Vaccine = Window.orderBy('Vaccine')
df_vaccine = df_vaccine.select('Vaccine').distinct()\
        .withColumn('Vaccine_ID', row_number().over(Window_Vaccine))\
        .select('Vaccine_ID', 'Vaccine')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_vaccine)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    df_animal.write.mode("overwrite").saveAsTable('dimAnimal')
    df_adopter.write.mode("overwrite").saveAsTable("dimAdopter")
    df_staff.write.mode("overwrite").saveAsTable("dimStaff")
    df_vaccine.write.mode("overwrite").saveAsTable("dimVaccine")
except:
    df_animal.write.mode("overwrite").option('mergeSchema', True).saveAsTable('dimAnimal')
    df_adopter.write.mode("overwrite").option('mergeSchema', True).saveAsTable("dimAdopter")
    df_staff.write.mode("overwrite").option('mergeSchema', True).saveAsTable("dimStaff")
    df_vaccine.write.mode("overwrite").option('mergeSchema', True).saveAsTable("dimVaccine")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
