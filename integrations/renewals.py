query = """
SELECT COUNT(PL.FamilyID)[value], N'xDM2XZVEBml' [dataElement] , FORMAT(PL.EnrollDate, 'yyyyMMdd') [period], L.LocationUUID orgUnit, CASE I.Gender WHEN 'M' THEN 'Male' WHEN 'F' THEN 'Female' END categoryOptionCombo, Prod.ProductCode attributeOptionCombo

FROM tblPolicy PL 
INNER JOIN tblProduct Prod ON PL.ProdID = Prod.ProdID
INNER JOIN tblFamilies F ON PL.FamilyId = F.FamilyID
INNER JOIN tblInsuree I ON F.InsureeID = I.InsureeID
INNER JOIN tblLocations L ON F.LocationId = L.LocationId 
	
WHERE PL.ValidityTo IS NULL
AND F.ValidityTo IS NULL
AND I.ValidityTo IS NULL
AND Prod.ValidityTo IS NULL
AND PL.PolicyStage = N'R'
AND PL.EnrollDate BETWEEN N'{date_from}' AND N'{date_to}'
AND I.Gender IN ('M','F')

GROUP BY FORMAT(PL.EnrollDate, 'yyyyMMdd'), Prod.ProductCode, L.LocationUUID, I.Gender
"""

parameters = {
    'orgUnitIdScheme': 'code',
    'dataElementIdScheme': 'uid',
    'categoryOptionComboIdScheme': 'code'
}
