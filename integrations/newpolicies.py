query = """

SET NOCOUNT ON;
	
SELECT COUNT(PL.FamilyID)[value], N'KxaZEz3G9mR' [dataElement] , FORMAT(PL.EnrollDate, 'yyyyMMdd') [period], L.LocationUUID orgUnit, CASE I.Gender WHEN 'M' THEN 'Male' WHEN 'F' THEN 'Female' END categoryOptionCombo, Prod.ProductCode attributeOptionCombo

FROM tblPolicy PL 
INNER JOIN tblFamilies F ON PL.FamilyId = F.FamilyID
INNER JOIN tblInsuree I ON F.InsureeID = I.InsureeID
INNER JOIN tblProduct Prod ON PL.ProdID = Prod.ProdID
INNER JOIN tblLocations L ON F.LocationId = L.LocationId
	
WHERE PL.ValidityTo IS NULL
AND F.ValidityTo IS NULL
AND I.ValidityTo IS NULL
AND Prod.ValidityTo IS NULL
AND L.ValidityTo IS NULL
AND PL.PolicyStage = N'N'
AND I.Gender IN ('M','F')
AND L.LocationName <> N'Funding'
AND PL.EnrollDate BETWEEN N'{date_from}' AND N'{date_to}'

GROUP BY FORMAT(PL.EnrollDate, 'yyyyMMdd'), Prod.ProductCode, L.LocationUUID, I.Gender

"""

parameters = {
    'orgUnitIdScheme': 'code',
    'dataElementIdScheme': 'uid',
    'categoryOptionComboIdScheme': 'code'
}
