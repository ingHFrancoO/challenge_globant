ALTER TABLE "fact_hires" ADD CONSTRAINT "fk_fact_date" FOREIGN KEY ("hired_at_id") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_hires" ADD CONSTRAINT "fk_fact_department" FOREIGN KEY ("department_id") REFERENCES "dim_department" ("department_id");

ALTER TABLE "fact_hires" ADD CONSTRAINT "fk_fact_job" FOREIGN KEY ("job_id") REFERENCES "dim_job" ("job_id");
