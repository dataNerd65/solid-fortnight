% Database connection predicate
:- dynamic db_item_available/4.

%Predicate to assert database items into Prolog
assert_db_items :-
retractall(db_item_available(_, _, _, _)), % Remove existing items from Prolog database
findall(item_available(Type, Brand, Model, Price, Quantity),
       db_item_available(Type, Brand, Model, Price, Quantity),
       Items),
       maplist(assertz, Items).


% Predicate to query if an item is available in the database
item_available(Type, Brand, Model, Price, Quantity) :-
db_item_available(Type, Brand, Model, Price, Quantity).
