
/*sqlzoo 
https://mubu.com/doc/rTZwIp5KG0

CASE()
COALESCE()
FIRST()
LAST()
LIMIT()
在某些数据库中， LEFT JOIN 称为 LEFT OUTER JOIN。*/


--（对啦，用自连接啊）列出連接115 和 137 ('Haymarket' 和 'Leith') 的公司名和路線號碼。不要重覆。
SELECT DISTINCT(a.company), a.num 
FROM route a JOIN route b ON 
(a.company = b.company AND a.num = b.num)
 JOIN stops stopsa ON (stopsa.id = a.stop) 
 JOIN stops stopsb ON  (stopsb.id = b.stop) 
WHERE stopsa.name = 'Haymarket' AND stopsb.name = 'Leith';


--（对啦）列出曾與演員亞特·葛芬柯'Art Garfunkel'合作過的演員姓名。
SELECT name
FROM movie JOIN casting ON movie.id=movieid 
JOIN actor ON actorid=actor.id  WHERE  movieid IN (SELECT movieid
FROM movie JOIN casting ON movie.id=movieid 
JOIN actor ON actorid=actor.id  WHERE name = 'Art Garfunkel') AND name != 'Art Garfunkel'


/*（对啦）列出演員茱莉·安德絲'Julie Andrews'曾參與的電影名稱及其第1主角。
是否列了電影 "Little Miss Marker"兩次?
她於1980再參與此電影Little Miss Marker. 原作於1934年,她也有參與。 電影名稱不是獨一的。在子查詢中使用電影編號。*/

SELECT title, name FROM (movie JOIN casting ON movie.id=movieid
         JOIN actor  ON actorid=actor.id)
WHERE movie.id IN
(SELECT movie.id FROM
  movie JOIN casting ON movie.id=movieid
         JOIN actor  ON actorid=actor.id
where name ='Julie Andrews') AND ord = 1



--（对啦，自己写了简便算法）尊·特拉華達'John Travolta'最忙是哪一年? 顯示年份和該年的電影數目。
SELECT yr,COUNT(title) FROM
  movie JOIN casting ON movie.id=movieid
         JOIN actor   ON actorid=actor.id
where name='John Travolta'
GROUP BY yr ORDER BY COUNT(title) DESC limit 1


-- 有借鉴意义的：
SELECT yr,COUNT(title) FROM
  movie JOIN casting ON movie.id=movieid
         JOIN actor   ON actorid=actor.id
where name='John Travolta'
GROUP BY yr
HAVING COUNT(title)=(SELECT MAX(c) FROM
(SELECT yr,COUNT(title) AS c FROM
   movie JOIN casting ON movie.id=movieid
         JOIN actor   ON actorid=actor.id
 where name='John Travolta'
 GROUP BY yr) AS t
)


--（对啦，可以连着JOIN）列出1962年首影的電影及它的第1主角。
SELECT title, name FROM casting JOIN movie ON (casting.movieid = movie.id) JOIN actor ON (casting.actorid = actor.id)
WHERE yr = 1962  AND ord = 1;

--（对啦，一步一步的做+扩展）好價大碟是指大碟中每一首歌曲的價格是少於5角。 找出好價大碟，列出大碟名字，售價和歌曲數量。
SELECT title, price, COUNT(song)
FROM track  JOIN album ON (asin=album)
WHERE price IS NOT NULL GROUP BY title, price HAVING price/COUNT(song)<0.5;


-- 找出歌曲收錄在２隻以上的大碟中。列出收錄次數（所以要用COUNT(DISTINCT title)，而不是COUNT(song)）。
SELECT song, COUNT(DISTINCT title)
FROM track  JOIN album ON (asin=album)
GROUP BY song
HAVING COUNT(DISTINCT title)>2;


--（对啦，这里用left join 是因为有的队伍没有goal）
SELECT mdate,
  team1, SUM(CASE WHEN teamid=team1 THEN 1 ELSE 0 END) score1,
team2, SUM(CASE WHEN teamid=team2 THEN 1 ELSE 0 END) score2
 FROM game LEFT JOIN goal ON matchid = id GROUP BY mdate, team1, team2 ORDER BY mdate, matchid, team1, team2;


--（自己没把 mdate 也加上，前面select关键词有两个，后面group by 也得有两个）：
SELECT matchid, mdate, COUNT( teamid )
  FROM game JOIN goal ON matchid = id 
 WHERE (team1 = 'POL' OR team2 = 'POL')
GROUP BY matchid, mdate

/*（对啦）
修改它，只列出全部賽事，射入德國龍門的球員名字。
找非德國球員的入球，德國可以在賽事中作team1 隊伍１（主）或team2隊伍２（客）。 你可以用teamid!='GER' 來防止列出德國球員。 你可以用DISTINCT來防止球員出現兩次以上。*/
-- （网上的）
SELECT DISTINCT(player)
FROM goal JOIN game
ON goal.matchid = game.id
WHERE (team1 = 'GER' or team2 = 'GER') AND teamid != 'GER';
--（自己的）SELECT DISTINCT(goal.player)
  FROM game JOIN goal ON (goal.teamid = game.team1 AND goal.matchid = game.id)
    WHERE (goal.teamid != 'GER' AND game.team2 = 'GER') 
UNION
SELECT DISTINCT(goal.player)
  FROM game JOIN goal ON (goal.teamid = game.team2 AND goal.matchid = game.id)
    WHERE (goal.teamid != 'GER' AND game.team1 = 'GER');


--（对啦）列出政黨名單，當中最少有一名黨員在議會內。
SELECT DISTINCT(party.name) FROM party 
INNER JOIN msp 
ON (party.code = msp.party) ;
--或者
SELECT party.name FROM party 
INNER JOIN msp 
ON (party.code = msp.party) GROUP BY party.name HAVING COUNT(msp.name)>=1;


--（对啦）使用COUNT 和 GROUP BY dept.name來顯示每一學系的老師數目。 使用 RIGHT JOIN 以確保工程系Engineering 是在當中。
SELECT  dept.name, COUNT(teacher.name)  FROM  teacher RIGHT JOIN dept ON (teacher.dept = dept.id)
 GROUP BY dept.name;


--（对啦）Use COALESCE to print the mobile number. Use the number '07986 444 2266' if there is no number given. Show teacher name and mobile number or '07986 444 2266'
SELECT teacher.name, COALESCE(teacher.mobile, '07986 444 2266') FROM teacher;
--或者
SELECT teacher.name, IFNULL(teacher.mobile, '07986 444 2266') FROM teacher;


--（对啦）哪年哪獎項，是同一獎項(subject)頒發給3個人。只列出2000年及之後的資料。SELECT yr, subject FROM nobel WHERE yr>=2000 GROUP BY yr, subject HAVING  COUNT(winner) = 3;


--（对啦）哪些得獎者獲獎多於1次呢？他們是哪一年獲得哪項獎項呢？ 列出他們的名字，獲獎年份及獎項。先按名字，再按年份順序排序。
SELECT winner, yr, subject FROM nobel
  WHERE winner IN (SELECT new.winner FROM
  (SELECT winner, COUNT(*) FROM nobel
    GROUP BY winner HAVING COUNT(*) > 1) AS new)
  ORDER BY winner, yr;
 

--（对啦）哪幾年的得獎者人數多於12人呢? 列出得獎人數多於12人的年份，獎項和得獎者。
SELECT yr, subject, winner FROM nobel
  WHERE yr IN (SELECT new.yr FROM (SELECT yr, COUNT(*) FROM nobel
  GROUP BY yr HAVING COUNT(*) > 12) AS new);


-- （对啦）哪幾年頒發了物理獎，但沒有頒發化學獎?
SELECT DISTINCT(yr) FROM nobel 
  WHERE yr IN 
  (SELECT yr FROM nobel 
  WHERE subject = 'Physics') AND yr NOT IN (SELECT yr FROM nobel WHERE subject = 'Chemistry');


--（对啦）13:Put the continents right...
Oceania becomes Australasia
Countries in Eurasia and Turkey go to Europe/Asia
Caribbean islands starting with 'B' go to North America, other Caribbean islands go to South America
Show the name, the original continent and the new continent of all countries.


SELECT name,continent,
CASE WHEN continent IN ('Eurasia', 'Turkey')
     THEN 'Europe/Asia'

     WHEN continent = 'Oceania'
     THEN 'Australasia'

     WHEN continent = 'Caribbean'
          THEN
          CASE
          WHEN name LIKE 'B%'
          THEN 'North America'
          ELSE 'South America'
          END
     ELSE continent
     END
FROM world
ORDER BY name ASC;


--（对啦）有些國家的人口是同洲份的所有其他國的3倍或以上。列出 國家名字name 和 洲份 continent。
SELECT name, continent FROM world x
  WHERE population/3 >= ALL((SELECT population FROM world y WHERE x.continent = y.continent AND x.name != y.name));


-- 找出洲份，當中全部國家都有少於或等於 25000000 人口. 在這些洲份中，列出國家名字name，continent 洲份和population人口。
SELECT name, continent, population FROM world x
 WHERE 25000000 >= ALL(SELECT population FROM world y WHERE 
 population > 0 AND x.continent = y.continent);


-- 列出洲份名稱，和每個洲份中國家名字按子母順序是排首位的國家名。(即每洲只有列一國)
SELECT continent, name FROM world x 
  WHERE name = (SELECT name FROM world y
  WHERE x.continent = y.continent ORDER BY name limit 1);


/*Germany德國（人口8000萬），在Europe歐洲國家的人口最多。Austria奧地利（人口850萬）擁有德國總人口的11％。
顯示歐洲的國家名稱name和每個國家的人口population。以德國的人口的百分比作人口顯示。*/
SELECT name, CONCAT(ROUND(100*population/(SELECT MAX(population) FROM world WHERE continent = 'Europe')), '%') FROM world WHERE continent = 'Europe';


