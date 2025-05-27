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
vaccine = DeltaTable.forName(spark, "SilverLayer.vaccinations" )

dimAnimal = DeltaTable.forName(spark, "GoldLayer.dimanimal")
dimAdopter = DeltaTable.forName(spark, "GoldLayer.dimAdopter")
dimVaccine = DeltaTable.forName(spark, "GoldLayer.dimVaccine")
dimStaff = DeltaTable.forName(spark, "GoldLayer.dimStaff")

df_animal = animal.toDF()
df_staff = staff.toDF()
df_person = person.toDF()
df_staff_asig = staff_asig.toDF()
df_adopter = adopter.toDF()
df_vaccine = vaccine.toDF()

df_dimAnimal = dimAnimal.toDF()
df_dimAdopter = dimAdopter.toDF()
df_dimVaccine = dimVaccine.toDF()
df_dimStaff = dimStaff.toDF()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_dimAdopter)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_fact_step1 = df_animal.select("Name", "Species", "Admission_Date").distinct()
df_fact_step1 = df_animal.join(df_dimAnimal, (df_animal.Name == df_dimAnimal.Name) & (df_animal.Species == df_dimAnimal.Species) ).select(df_dimAnimal.Animal_Id, df_dimAnimal.Name, df_dimAnimal.Species, df_animal.Admission_Date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_fact_step2 = df_fact_step1.join(df_adopter, (df_fact_step1.Name == df_adopter.Name) & (df_fact_step1.Species == df_adopter.Species), "left" )\
    .join(df_dimAdopter, (df_adopter.Adopter_Email == df_dimAdopter.Adopter_Email), "left" )\
    .select("Animal_Id", df_fact_step1["Name"], df_fact_step1["Species"], "Admission_Date", df_dimAdopter["Adopter_Email"], "Adopter_ID", "Adoption_Fee" ) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_fact_step2)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_fact_step3 = df_fact_step2.join(df_vaccine, (df_fact_step2.Name == df_vaccine.Name) & (df_fact_step2.Species == df_vaccine.Species), "left" ).select("Animal_Id", df_fact_step1["Name"], df_fact_step1["Species"], "Admission_Date", df_dimAdopter["Adopter_Email"], "Adopter_ID", "Adoption_Fee", "Vaccine" ,"Vaccination_Time")\
.join(df_dimVaccine,df_vaccine.Vaccine == df_dimVaccine.Vaccine, "left" ).select("Animal_Id", df_fact_step1["Name"], df_fact_step1["Species"], "Admission_Date", df_dimAdopter["Adopter_Email"], "Adopter_ID", "Adoption_Fee", df_dimVaccine["Vaccine"] ,"Vaccination_Time", "Vaccine_ID")

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

df_fact_vaccination_step1 = df_vaccine.join(df_dimAnimal, (df_vaccine.Name == df_dimAnimal.Name) & (df_vaccine.Species == df_dimAnimal.Species), "left" ).select(df_dimAnimal.Animal_Id, df_vaccine.Vaccination_Time, df_vaccine.Vaccine, df_vaccine.Batch, df_vaccine.Email).distinct() 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_fact_vaccination_step2 = df_fact_vaccination_step1.join(df_dimVaccine, df_fact_vaccination_step1.Vaccine == df_dimVaccine.Vaccine).select(df_dimAnimal.Animal_Id, df_vaccine.Vaccination_Time, df_dimVaccine.Vaccine_ID, df_vaccine.Batch, df_vaccine.Email)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_fact_vaccination_step3 = df_fact_vaccination_step2.join(df_dimStaff, df_fact_vaccination_step2.Email == df_dimStaff.Email).select(df_dimAnimal.Animal_Id, df_vaccine.Vaccination_Time, df_dimVaccine.Vaccine_ID, df_vaccine.Batch, df_dimStaff.Staff_Id)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    df_fact_step2.write.mode("overwrite").saveAsTable('Fact_AnimalShelterDetails')
    df_fact_vaccination_step3.write.mode("overwrite").saveAsTable("Fact_AnimalShelter_Vaccinations")
except:
    print("Issue in writing Fact data")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
