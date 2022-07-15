query = """
SELECT CAST(SUM(PR.Amount) AS NVARCHAR(30))[value], 'dQxo7a1fQNL' dataElement, FORMAT(PR.PayDate, 'yyyyMMdd') [period], L.LocationUUID orgUnit, PR.PayType categoryOptionCombo, ProductCode attributeOptionCombo

FROM tblPremium PR 
INNER JOIN tblPolicy PL ON PR.PolicyID = PL.PolicyID
INNER JOIN tblProduct Prod ON PL.ProdID = Prod.ProdId
INNER JOIN tblFamilies F ON PL.FamilyID = F.FamilyID
INNER JOIN tblLocations L ON F.LocationId = L.LocationID 

WHERE PR.ValidityTo IS NULL 
AND PL.ValidityTo IS NULL 
AND F.ValidityTo IS NULL
AND PR.PayDate BETWEEN N'{date_from}' AND N'{date_to}'  

GROUP BY PR.PayDate, L.LocationUUID, PR.PayType, ProductCode
"""

parameters = {
    'orgUnitIdScheme': 'code',
    'dataElementIdScheme': 'uid',
    'categoryOptionComboIdScheme': 'code'
}
