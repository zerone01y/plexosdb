SELECT c.name AS class, cat.name AS category, cat.rank
FROM t_category cat
LEFT JOIN t_class c ON cat.class_id = c.class_id
${where_clause}
