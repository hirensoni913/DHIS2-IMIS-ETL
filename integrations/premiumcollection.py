query = """
SELECT CAST(SUM(PR.Amount) AS NVARCHAR(30))[value], 'dQxo7a1fQNL' dataElement, FORMAT(PR.PayDate, 'yyyyMMdd') [period], L.LocationUUID orgUnit, PR.PayType categoryOptionCombo, ProductCode attributeOptionCombo

FROM tblPremium PR LEFT OUTER JOIN tblPayer Pay ON PR.PayerId = Pay.PayerId
INNER JOIN tblPolicy PL ON PR.PolicyID = PL.PolicyID
INNER JOIN tblProduct Prod ON PL.ProdID = Prod.ProdId
INNER JOIN tblOfficer O ON PL.OfficerID = O.OfficerID
INNER JOIN tblDistricts DO ON O.LocationId = DO.DistrictID
INNER JOIN tblFamilies F ON PL.FamilyID = F.FamilyID
INNER JOIN tblVillages V ON V.VillageId = F.LocationId
INNER JOIN tblWards W ON W.WardId = V.WardId
INNER JOIN tblDistricts FD ON FD.DistrictID = W.DistrictID
INNER JOIN tblRegions R ON R.RegionId = FD.Region
INNER JOIN tblLocations L ON V.VillageId = L.LocationID 
WHERE PR.ValidityTo IS NULL 
AND Pay.ValidityTo IS NULL 
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
