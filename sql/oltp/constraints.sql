ALTER TABLE "hired_employees" ADD CONSTRAINT "fk_hired_employees_department" FOREIGN KEY ("department_id") REFERENCES "departments" ("id");

ALTER TABLE "hired_employees" ADD CONSTRAINT "fk_hired_employees_job" FOREIGN KEY ("job_id") REFERENCES "jobs" ("id");
