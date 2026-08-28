# Resume file

Drop your resume PDF in this folder as `resume.pdf` (or set `RESUME_FILE_NAME`
in `.env` to a different filename). The site's "Download Resume" / "View
Resume" buttons look for `media/resume/<RESUME_FILE_NAME>` and hide
themselves automatically if the file isn't there yet — nothing else to wire
up.
