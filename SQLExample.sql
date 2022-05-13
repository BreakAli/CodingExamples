-- This is a SQL query that finds the percentage drop in CTA ridership on the Blue Line due to Covid

SELECT Round(SUM(PreCOVIDAvgF)/Count(Name),0) AS PreCOVIDAvg, 
	   Round(SUM(PostCOVIDAvgF)/Count(Name),0) AS PostCOVIDAvg, 
	   Round((SUM(PreCOVIDAvgF)/Count(Name))-(SUM(PostCOVIDAvgF)/Count(Name)),0) AS Decrease, 
	   Round((((SUM(PreCOVIDAvgF)/Count(Name))-(SUM(PostCOVIDAvgF)/Count(Name))) / (SUM(PreCOVIDAvgF)/Count(Name))) * 100,2) AS PercentDrop
FROM
(
	SELECT AvgBlueLineBefore.Name, PreCOVIDAvg AS PreCOVIDAvgF, PostCOVIDAvg AS PostCOVIDAvgF, PreCOVIDAvg-PostCOVIDAvg AS Decrease1, ((PreCOVIDAvg-PostCOVIDAvg) / PreCOVIDAvg) * 100 AS PercentDropF
	FROM
	(
		SELECT StationID, Name, (S/Count) AS PreCOVIDAvg
		FROM
		(
			SELECT subquery.StationID, subquery.Name,(SELECT SUM(subquery.DailyTotal) ) S, COUNT(*) As Count
			FROM 
			(
				SELECT Stations.StationID, Stations.Name, Riderships.TheDate, Riderships.DailyTotal
				FROM Stations
				JOIN Riderships
				ON Stations.StationID = Riderships.StationID
				WHERE (Stations.Name LIKE '%Blue%')  AND TheDate < '2020-03-01'
				
			) AS subquery
			GROUP BY Name,StationID
		) AS BlueLineBefore
	)AS AvgBlueLineBefore
	
	JOIN
	
	( 
		SELECT Name, (Z/Count2) AS PostCOVIDAvg
		FROM
		(
			SELECT subquery.StationID, subquery.Name, (SELECT SUM(subquery.DailyTotal)) Z, COUNT(*) As Count2
			FROM 
			(
				SELECT Stations.StationID, Stations.Name, Riderships.TheDate, Riderships.DailyTotal
				FROM Stations
				JOIN Riderships
				ON Stations.StationID = Riderships.StationID
				WHERE Stations.Name LIKE '%Blue%' AND TheDate >= '2020-03-01'
				
			) AS subquery
			GROUP BY Name,StationID
		) AS BlueLineAfter

	) AS AvgBlueLineAfter

	ON AvgBlueLineBefore.name = AvgBlueLineAfter.name 
	ORDER BY AvgBlueLineBefore.StationID

) AS Final;
