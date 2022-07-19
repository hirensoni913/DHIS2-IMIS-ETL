query = """
SELECT COUNT(1)[value], N'qu7fou3ix7h' dataElement, FORMAT(ISNULL(C.DateTo, C.DateFrom), 'yyyyMMdd') [period], HF.HfUUID orgUnit
FROM tblClaim C  
INNER JOIN tblHF HF ON C.HFID = HF.HFID
WHERE C.ValidityTo IS NULL 
AND HF.ValidityTo IS NULL
AND C.ClaimStatus <> 2
AND ISNULL(C.DateTo, C.DateFrom) BETWEEN N'{date_from}' AND N'{date_to}'
GROUP BY ISNULL(C.DateTo, C.DateFrom),HF.HfUUID
"""

parameters = {
    'orgUnitIdScheme': 'code',
    'dataElementIdScheme': 'uid'
}
