query = """
SELECT HF.HfUUID Code, '_HF - ' + HF.HFName  + ' (' + HF.HFCode + ')' [Name], HF.HFName ShortName, '1900-01-01' OpeningDate, L.LocationUUID ParentId
FROM tblHF HF
INNER JOIN tblLocations L ON HF.LocationId = L.LocationId
WHERE HF.ValidityTo IS NULL
AND L.ValidityTo IS NULL
"""
