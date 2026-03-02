SELECT
	obj.name AS object,
	parent_class.name AS parent_class,
	child_class.name AS child_class,
	coll.name AS collection,
	prop.name AS property,
	r.phase_id,
	r.report_period,
	r.report_summary,
	r.report_statistics,
	r.report_samples,
	r.write_flat_files
FROM t_report r
LEFT JOIN t_object obj ON r.object_id = obj.object_id
LEFT JOIN t_property_report prop ON r.property_id = prop.property_id
LEFT JOIN t_collection coll ON prop.collection_id = coll.collection_id
LEFT JOIN t_class parent_class ON coll.parent_class_id = parent_class.class_id
LEFT JOIN t_class child_class ON coll.child_class_id = child_class.class_id
${where_clause}
