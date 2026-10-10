GRAMMAR = r"""
?start: policy
policy: "CERTIFY" theta ":" ID "REQUIRE" expr
theta: "DEPLOYMENT" -> deployment | "ANSWER" -> answer | "LOAD" -> load | "PROOF" -> proof
?expr: or_expr
?or_expr: and_expr | or_expr "OR" and_expr -> or_
?and_expr: clause | and_expr "AND" clause -> and_
?clause: "EXISTS" "PATH" path ("WHERE" psi)? -> exists_path
       | "FOR" "ALL" ID "IN" ID ":" clause   -> forall
       | "(" expr ")"
path: node (arrow edge arrow node)*
node: ":" "(" ID ")"
edge: "[" ID "]"
arrow: "->"
psi: psi "AND" psi -> psi_and | "NOT" psi_atom -> psi_not | psi_atom
psi_atom: ID "." ID "=" value -> eq
        | ID "." ID "IN" ID -> in_
        | ID "." ID "CONTAINS" value -> contains
        | ID "." ID "ALLOWS" ID -> allows
        | ID "." ID "IS_CERTIFIED" -> is_certified
        | ID "." ID "HAS_NO_UNAPPROVED_IMPORTS" -> no_unapproved_imports
value: STRING | ID | NUMBER
ID: /[A-Za-z_][A-Za-z0-9_]*/
STRING: /"[^"]*"/
NUMBER: /[0-9]+(\.[0-9]+)?/
%import common.WS
%ignore WS
"""
