query = """
SET NOCOUNT ON;
DECLARE @CategoryOptionCombo TABLE (Gender NVARCHAR(1), MinAge INT, MaxAge INT, DHISUID NVARCHAR(11))
INSERT INTO @CategoryOptionCombo (Gender, MinAge, MaxAge, DHISUID) VALUES
(N'F',	1, 10, N'RN3dfJ6lomx'),
(N'F',	11, 20, N'xGYZVLi3TcN'),
(N'F',	0, 1, N'N25TKL5Nviz'),
(N'F',	21, 30, N'DfTj9lOfO4E'),
(N'F',	31, 40, N'C4l1efjuZ7z'),
(N'F',	41, 50, N'z2vDhK4R9w2'),
(N'F',	51, 60, N'i6WGfRsv0eH'),
(N'F',	61, 150, N'hc4D9jQQ5aH'),
(N'M',	1, 10, N'XWivMQbogJM'),
(N'M',	11, 20, N'RjO2pJqSNyF'),
(N'M',	0, 1, N'JImXfiX3417'),
(N'M',	21, 30, N'MD5erPl1Xr1'),
(N'M',	31, 40, N'WMHoo50RtWn'),
(N'M',	41, 50, N'ITuSXcDACWo'),
(N'M',	51, 60, N'VcVrGL5Arrj'),
(N'M',	61, 150, N'QURu6L1C4yj')

SELECT COUNT(I.InsureeID) [value], N'cxBAJmLgdTu' dataElement, FORMAT(PL.EnrollDate, 'yyyyMMdd') [period], L.LocationUUID orgUnit, doc.DHISUID categoryOptionCombo

FROM tblPolicy PL INNER JOIN tblInsuree I ON PL.FamilyID = I.FamilyID
INNER JOIN tblFamilies F ON PL.FamilyID = F.FamilyID
INNER JOIN tblInsureePolicy InsPL ON InsPL.InsureeId = I.InsureeId AND InsPL.PolicyId = PL.PolicyID
INNER JOIN tblLocations L ON L.LocationId = F.LocationId
INNER JOIN @CategoryOptionCombo doc ON I.Gender = doc.Gender AND DATEDIFF(DAY, I.DOB, PL.EnrollDate)/365 BETWEEN doc.MinAge AND doc.MaxAge

WHERE PL.ValidityTo IS NULL 
AND I.ValidityTo IS NULL 
AND F.ValidityTo IS NULL
AND InsPL.ValidityTo IS NULL
AND L.ValidityTo IS NULL
AND L.LocationName <> N'Funding'
AND I.IsHead = 1
AND PL.EnrollDate BETWEEN N'{date_from}' AND N'{date_to}'

GROUP BY FORMAT(PL.EnrollDate, 'yyyyMMdd'), L.LocationUUID, doc.DHISUID 
 
"""
parameters = {
    'orgUnitIdScheme': 'code',
    'dataElementIdScheme': 'uid',
    'categoryOptionComboIdScheme': 'uid'
}
