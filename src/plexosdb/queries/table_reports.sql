SELECT r.report_id, r.name AS report_name, to2.name AS profile_object, r.description
FROM t_report r
LEFT JOIN t_object to2 ON r.profile_object_id = to2.object_id
${where_clause}
