"""tests_reporting - Tests for reporting.py"""

from asciireqs.fields import LINE_NO
from asciireqs.reporting import *


def doc1_reqs() -> Requirements:
    return {'D1-1': {fields.ID: 'D1-1', LINE_NO: 3}, 'D1-2': {fields.ID: 'D1-2', LINE_NO: 7}}


def docs_with_req_prefix() -> ReqDocument:
    doc = ReqDocument()
    doc.req_prefix = 'UR-REQ-'
    doc.name = 'ur-reqs.adoc'
    child_doc1 = ReqDocument()
    child_doc1.req_prefix = 'SW-REQ-'
    child_doc1.name = 'sw-reqs.adoc'
    doc.add_child_doc(child_doc1)
    child_doc2 = ReqDocument()
    child_doc2.req_prefix = 'HW-REQ-'
    child_doc2.name = 'hw-reqs.adoc'
    doc.add_child_doc(child_doc2)
    return doc


def test_line_numbers_for_requirements() -> None:
    lines = line_numbers_for_requirements(doc1_reqs())
    assert lines == {3: 'D1-1', 7: 'D1-2'}


def test_get_spec_hierarchy() -> None:
    lines = get_spec_hierarchy(docs_with_req_prefix(), '')
    assert len(lines) == 3
    assert lines[0] == '* ur-reqs.adoc\n'
    assert lines[1] == '** sw-reqs.adoc\n'
    assert lines[2] == '** hw-reqs.adoc\n'


def test_insert_requirement_links() -> None:
    doc = docs_with_req_prefix()
    assert insert_requirement_links('This is the UR-REQ-001 requirement', doc)\
           == 'This is the xref:ur-reqs.adoc#UR-REQ-001[UR-REQ-001] requirement'
    assert insert_requirement_links('This is the SW-REQ-002 requirement', doc) \
           == 'This is the xref:sw-reqs.adoc#SW-REQ-002[SW-REQ-002] requirement'


def test_insert_anchor() -> None:
    doc = docs_with_req_prefix()
    assert insert_anchor('| SW-REQ-001', 'SW-REQ-001', doc) == '| [[SW-REQ-001]]SW-REQ-001'
    assert insert_anchor('| SW-REQ-001 | UR-REQ-002', 'SW-REQ-001', doc)\
           == '| [[SW-REQ-001]]SW-REQ-001 | xref:ur-reqs.adoc#UR-REQ-002[UR-REQ-002]'


def test_has_element() -> None:
    s = 'One, Two,Three'
    assert has_element(s, 'One')
    assert has_element(s, 'Three')
    assert not has_element(s, 'Four')
    assert not has_element(s, 'Two,Three')


def test_split_req_list() -> None:
    assert split_req_list('One, Two,Three') == ['One', 'Two', 'Three']
