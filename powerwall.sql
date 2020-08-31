CREATE TABLE public."PollData"
(
    "PollTime" timestamp with time zone NOT NULL,
    "DataSource" character varying(110) COLLATE pg_catalog."default",
    "JsonData" text COLLATE pg_catalog."default",
    "PollID" integer NOT NULL DEFAULT nextval('"PollData_PollID_seq"'::regclass),
    CONSTRAINT "PollData_pkey" PRIMARY KEY ("PollID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."PollData"
    OWNER to postgres;

COMMENT ON TABLE public."PollData"
    IS 'The table that receives the polling data';

COMMENT ON COLUMN public."PollData"."PollTime"
    IS 'Time we captured data.  There may be multiple rows with the same poll time.  But each should have a different source.';

COMMENT ON COLUMN public."PollData"."DataSource"
    IS 'The source of the data.  This can be something like the API or rest method that retrieved the data';

COMMENT ON COLUMN public."PollData"."JsonData"
    IS 'The JSON data captured ';

COMMENT ON COLUMN public."PollData"."PollID"
    IS 'Unique ID of poll';
-- Index: PollTime_idx

-- DROP INDEX public."PollTime_idx";

CREATE INDEX "PollTime_idx"
    ON public."PollData" USING btree
    ("PollTime" ASC NULLS LAST)
    INCLUDE("PollTime")
    TABLESPACE pg_default;