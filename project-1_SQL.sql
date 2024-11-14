use ig_clone;

-- Find the 5 oldest users.
select username from users
order by created_at asc
limit 5;

-- What day of the week do most users register on? We need to figure out when to schedule an ad campaign?
select dayname(created_at) as user_registered, count(*) as cnt
from users
group by user_registered
order by cnt desc
limit 1;

-- We want to target our inactive users with an email campaign.Find the users who have never posted a photo
select username
from users as u
left join photos as p
on u.id = p.user_id
where u.id not in(select user_id from photos);

-- We're running a new contest to see who can get the most likes on a single photo.WHO WON??!!
SELECT uu.username,pp.image_url, COUNT(*) AS most_likes
FROM photos AS pp
JOIN likes AS ll
USING (user_id)
JOIN users AS uu
USING (id)
GROUP BY uu.username,pp.image_url
ORDER BY COUNT(*) DESC;

-- Our Investors want to know… How many times does the average user post?HINT - *total number of photos/total number of users*
select 
    (select count(*) from photos) / (select count(*) from users) as average;

-- user ranking by postings higher to lower
with cte1 as
(select user_id,count(user_id),
rank() over(order by count(user_id) desc) as rank_value
from photos
group by user_id),
cte2 as
(select * from cte1 as c1
left join users as u
on c1.user_id=u.id)
select * from cte2 as c2;

-- total numbers of users who have posted at least one time
select count(distinct user_id) from photos;

-- A brand wants to know which hashtags to use in a post
select tag_name,count(tag_name) as hashtag
from tags
group by tag_name
order by hashtag desc
limit 1;

-- What are the top 5 most commonly used hashtags?
select tag_name,count(tag_name) as cnt
from tags
group by tag_name
order by cnt desc
limit 5;

-- We have a small problem with bots on our site...Find users who have liked every single photo on the site.
select * from users;
select * from photos;
select * from likes;

SELECT username, COUNT(*) AS num_likes
FROM users
JOIN likes ON users.id = likes.user_id
GROUP BY likes.user_id
HAVING num_likes = (SELECT COUNT(*) FROM photos);


-- Find users who have never commented on a photo.
select username
from users as u
left join likes as l
on u.id = l.user_id
where u.id not in(select user_id from comments);


SELECT username
FROM users
WHERE id NOT IN (SELECT DISTINCT user_id
FROM comments
WHERE user_id IS NOT NULL);

end