--Create a new stored procedure called 'add_coord_columns' in schema 'dbo'
--Drop the stored procedure if it already exists
IF EXISTS (
SELECT *
    FROM INFORMATION_SCHEMA.ROUTINES
WHERE SPECIFIC_SCHEMA = N'dbo'
    AND SPECIFIC_NAME = N'add_coord_columns'
)
DROP PROCEDURE dbo.add_coord_columns
GO
-- Create the stored procedure in the specified schema
CREATE PROCEDURE dbo.add_coord_columns
    @param1 /*parameter name*/ int /*datatype_for_param1*/ = 0, /*default_value_for_param1*/
    @param2 /*parameter name*/ int /*datatype_for_param1*/ = 0 /*default_value_for_param2*/
-- add more stored procedure parameters here
AS
    -- body of the stored procedure
    SELECT @param1, @param2
    -- Drop 'ColumnNames' from table 'umts_transmitter' in schema 'dbo'
    ALTER TABLE dbo.umts_transmitter
    DROP COLUMN radian_lat, radian_lon, radian_azim, 
    onedp_lat, onedp_lon, twodp_lat, twodp_lon, coverage

    GO
    -- Add a new columns to table umts_transmitter in schema dbo
    ALTER TABLE dbo.umts_transmitter
    ADD radian_lat FLOAT , radian_lon FLOAT, radian_azim FLOAT, 
    onedp_lat FLOAT, onedp_lon FLOAT, twodp_lat FLOAT, twodp_lon FLOAT, coverage VARCHAR

--
GO
-- example to execute the stored procedure we just created
EXECUTE dbo.add_coord_columns 1 /*value_for_param1*/, 2 /*value_for_param2*/
GO



-- Create a new stored procedure called 'etl_transformation' in schema 'dbo' for updating created coordinates columns
-- such as (onedp_lat, onedplon, twodp_lat, twodp_lon, coverage)
-- Drop the stored procedure if it already exists
IF EXISTS (
SELECT *
    FROM INFORMATION_SCHEMA.ROUTINES
WHERE SPECIFIC_SCHEMA = N'dbo'
    AND SPECIFIC_NAME = N'etl_transformation'
)
DROP PROCEDURE dbo.etl_transformation
GO
-- Create the stored procedure in the specified schema
CREATE PROCEDURE dbo.etl_transformation
    @param1 /*parameter name*/ int /*datatype_for_param1*/ = 0, /*default_value_for_param1*/
    @param2 /*parameter name*/ int /*datatype_for_param1*/ = 0 /*default_value_for_param2*/
-- add more stored procedure parameters here
AS
    -- body of the stored procedure
    SELECT @param1, @param2
    -- UPDATE dbo.umts_transmitter
    -- SET radian_lat = RADIANS(latitude), radian_lon = RADIANS(longitude), radian_azim = RADIANS(azimuth), 
    -- onedp_lat = ROUND(latitude, 1), onedp_lon = ROUND(longitude, 1), twodp_lat = ROUND(latitude, 2), twodp_lon = ROUND(longitude, 2),
    -- coverage = 'macro';

    SELECT top 30 * from dbo.umts_transmitter;

   
GO
--example to execute the stored procedure we just created
EXECUTE dbo.etl_transformation 1 /*value_for_param1*/, 2 /*value_for_param2*/
GO
