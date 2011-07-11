clean:
	find ./ -name "*~" -exec rm {} \;
	find ./ -name "*.pyc" -exec rm {} \;
	find ./ -name "*.pyo" -exec rm {} \;
	find . -name "*.sw[op]" -exec rm {} \;
	rm -rf MSG.backup _trial_temp/ build/ dist/ MANIFEST \
		CHECK_THIS_BEFORE_UPLOAD.txt *.egg-info


stat:
	@echo "Changes:"
	@cat MSG
	@echo
	@echo "Bazzar working dir status:"
	@echo
	@echo -n "Current revision: "
	@bzr revno
	@bzr stat


# XXX this target isn't working...
todo:
	@echo `find .|xargs grep -2 XXX`


build:
	python setup.py build
	python setup.py sdist


check-docs: files = "docs/USAGE.txt"
check-docs:
	@python -c \
	"from ballotbox.testing import suite;suite.runDocTests('$(files)');"


check: build check-docs check-patterns
	trial ballotbox


commit: check
	bzr commit --show-diff


commit-msg: check
	bzr commit --file=MSG


push: commit
	bzr push lp:ballotbox


push-msg: commit-msg
	bzr push lp:ballotbox
	mv MSG MSG.backup
	touch MSG


upload: check
	python setup.py sdist upload --show-response
