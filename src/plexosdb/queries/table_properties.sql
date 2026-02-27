WITH text_agg AS (
SELECT
	tt.data_id,
	MAX(CASE 
                WHEN tc.name = 'Data File'
                THEN tt.value
            END) AS datafile_text,
	MAX(CASE 
                WHEN tc.name = 'Timeslice'
                THEN tt.value
            END) AS timeslice_text,
	tc.name as class_name
FROM
	t_text tt
LEFT JOIN t_class tc ON
	tt.class_id = tc.class_id
GROUP BY
	tt.data_id
    )
    ,    
tag_agg AS (
SELECT
	tg.data_id,
	MAX(CASE 
                WHEN tc.name = 'Data File'
                THEN '{Object}' || o.name
            END) AS datafile_tag,
	MAX(CASE 
                WHEN tc.name = 'Timeslice'
                THEN '{Object}' || o.name
            END) AS timeslice_tag,
	MAX(CASE 
                WHEN tc.name = 'Scenario'
                THEN '{Object}' || o.name
            END) AS scenario_tag,
	MAX(CASE 
                WHEN tc.name = 'Variable'
                THEN '{Object}' || o.name
            END) AS variable_tag,
	MAX(ta.action_symbol) as action
FROM
	t_tag tg
LEFT JOIN t_object o ON
	tg.object_id = o.object_id
LEFT JOIN t_class tc ON
	o.class_id = tc.class_id
LEFT JOIN t_action ta on
	tg.action_id = ta.action_id 
GROUP BY
	tg.data_id
ORDER BY
	tc.class_id  
	)
    SELECT
	parent_class.name AS parent_class,
	child_class.name AS child_class,
	coll.name AS collection,
	parent_obj.name AS parent_object,
	child_obj.name AS child_object,
	prop.name AS property,
	unit.value AS unit,
	IFNULL(band.band_id, 1) AS band_id,
	d.value AS value,
	date_from.date AS date_from,
	date_to.date AS date_to,
	COALESCE(tag_agg.timeslice_tag,
    text_agg.timeslice_text) AS pattern,
	tag_agg.action as action,
	tag_agg.variable_tag AS expression,
	COALESCE(tag_agg.datafile_tag,
             text_agg.datafile_text) AS filename,
	tag_agg.scenario_tag AS scenario,
	memo.value AS memo
FROM
	t_data d
--- mem ---
JOIN t_membership mem ON
	d.membership_id = mem.membership_id
LEFT JOIN t_object AS child_obj ON
	mem.child_object_id = child_obj.object_id
LEFT JOIN t_object AS parent_obj ON
	mem.parent_object_id = parent_obj.object_id
LEFT JOIN t_class AS child_class ON
	mem.child_class_id = child_class.class_id
LEFT JOIN t_class AS parent_class ON
	mem.parent_class_id = parent_class.class_id
LEFT JOIN t_collection AS coll ON
	mem.collection_id = coll.collection_id
--- data ---
LEFT JOIN t_band AS band ON
	d.data_id = band.data_id
LEFT JOIN t_property AS prop ON
	d.property_id = prop.property_id
LEFT JOIN t_unit AS unit ON
	prop.unit_id = unit.unit_id
LEFT JOIN t_date_from AS date_from ON
	d.data_id = date_from.data_id
LEFT JOIN t_date_to AS date_to ON
	d.data_id = date_to.data_id
LEFT JOIN t_memo_data AS memo on
	d.data_id = memo.data_id
--- cte: tag ---
LEFT JOIN tag_agg AS tag_agg ON
	d.data_id = tag_agg.data_id
--- cte: text ---
LEFT JOIN text_agg AS text_agg ON
	text_agg.data_id = d.data_id
ORDER BY
	parent_class,
	collection,
	parent_object,
	child_object