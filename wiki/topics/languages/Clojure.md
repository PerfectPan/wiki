---
title: Clojure
type: topic
category: languages
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - clojure
source_refs:
  - raw/sources/Clojure.md
---
# Clojure

- TODO 异步事件处理？
- 论坛：https://www.reddit.com/r/Clojure/
- ```clojure
  ;; Declares a namespace which sets a unique name for your functions
  ;; Since Clojure runs on the JVM we have to
  ;; define a class
  (ns clojure-tut.core
    (:require [clojure.string :as str])
    (:gen-class))

  ;; VARIABLES
  ;; Variables are immutable (value can't change) and they are
  ;; defined with def and start with letters or underscores
  ;; and can contain numbers also

  (def randVar 10)

  ;; DATA TYPES
  ;; Types are assigned based on the value assigned

  ;; -9,223,372,036,854,775,808 to +9,223,372,036,854,775,807
  (def aLong 15) 

  ;; 4.94065645841246544e-324d to 1.79769313486231570e+308d
  (def aDouble 1.23456)

  ;; A String
  (def aString "Hello")

  ;; true or false
  (def aBool true)

  ;; Get the data type
  (type 15)

  ;; Check if no value (nil)
  (nil? aLong)

  ;; Check if a value is positive
  (pos? aLong)

  ;; Check if a number is negative
  (neg? aLong)

  ;; Check if even
  (even? aLong)

  ;; Check if odd
  (odd? aLong)

  ;; Check if number
  (number? aLong)

  ;; Check if integer
  (integer? aLong)

  ;; Check if float
  (float? aLong)

  ;; Check if zero
  (zero? aLong)

  ;; FORMATTED OUTPUT

  (format "This is a string %s" aString)

  (format "5 spaces and %5d" aLong)

  (format "Leading zeros %04d" aLong)

  (format "%-4d left justified" aLong)

  (format "3 decimals %.3f" aDouble)

  ;; STRINGS
    (def str1 "This is my 2nd string")

  ;; Check if blank
  (str/blank? str1)

  ;; Does string contain "my"
  (str/includes? str1 "my")

  ;; Index of match
  (str/index-of str1 "my")

  ;; Split string into vector using separator or Regex
  (str/split str1 #" ")
  (str/split str1 #"\d")

  ;; Join a collection into 1 string with a seperator
  (str/join " " ["The" "Big" "Cheese"])

  ;; Replace all Regex with a string
  ;; There is also replace-first
  (str/replace "I am 42"  #"42" "43")

  ;; Remove whitespace at beginning and end
  ;; Also remove newlines with trim-newline
  ;; Remove left white space triml
  ;; and right trimr
  (str/trim str1)

  ;; Uppercase
  (str/upper-case str1)

  ;; Lowercase
  (str/lower-case str1)

  ;; LISTS
  ;; Stores a list of values with multiple data types

  (println (list "Dog" 1 3.4 true))

  ;; Get 1st Value
  (println (first (list 1 2 3)))

  ;; Get rest of values
  (println (rest (list 1 2 3)))

  ;; Get defined index
  (println (nth (list 1 2 3) 1))

  ;; Add values to the right
  (println (list* 1 2 [3 4]))

  ;; Add 1 value to the left
  (println (cons 3 (list 1 2)))

  ;; SETS
  ;; List of unique values

  (println (set '( 1 1 2)))

  ;; Get an index
  (println (get (set '(3 2)) 2))

  ;; Append a value
  (println (conj (set '(3 2)) 1))

  ;; Is value in set
  (println (contains? (set '(3 2)) 3))

  ;; Remove value from set
  (println (disj (set '(3 2)) 2))

  ;; VECTORS

  (println (vector 1 "Dog"))

  ;; Get index
  (println (get (vector 3 2) 1))

  ;; Append element
  (println (conj (vector 1 2) 3))

  ;; Remove 1st item
  (println (pop (vector 3 2)))

  ;; Return vector from one point to another
  (println (subvec (vector 1 2 3 4) 1 3))

  ;; MAPS
  ;; Collection of key value pairs

  (println (hash-map "Name" "Derek" "Age" 42))

  ;; Sorted lists sort based on keys
  (println (sorted-map 3 42 2 "Banas" 1 "Derek"))

  ;; Return value mapped to key
  (println (get (hash-map "Name" "Derek") "Name"))

  ;; Get value for the key
  (println (find (hash-map "Name" "Derek" "Age" 42) "Name"))

  ;; Does map contain a key
  (println (contains? (hash-map "Name" "Derek") "Age"))

  ;; Get list of keys
  (println (keys (hash-map "Name" "Derek" "Age" 42)))

  ;; Get values
  (println (vals (hash-map "Name" "Derek" "Age" 42)))

  ;; Merge maps
  (println (merge-with + (hash-map "Name" "Derek") (hash-map "Age" 42)))

  ;; ATOMS
  ;; With atoms you can change a variables value

  (defn atom-ex
    [x]

    ;; Define the atoms value
    (def atomEx (atom x))

    ;; Watchers can be attached to atoms and agents
    ;; to run functions when a value changes
    (add-watch atomEx :watcher
               (fn [key atom old-state new-state]
                 (println "atomEx changed from " old-state " to " new-state)))

    ;; Print the value
    (println "1st x" @atomEx)

    ;; Change the value
    (reset! atomEx 10)
    (println "2nd x" @atomEx)

    ;; Change the value using a function
    (swap! atomEx inc)
    (println "Increment x" @atomEx)
    )

  ;; AGENTS
  ;; Agents allow you to change values using functions

  (defn agent-ex
    []

    ;; Create agent
    (def tickets-sold (agent 0))

    ;; Add a value to an agent
    (send tickets-sold + 15)

    ;; Added because there is a delay often
    (println)
    (println "Tickets " @tickets-sold)

    ;; Wait for the value to update with await-for
    (send tickets-sold + 10)
    (await-for 100 tickets-sold)
    (println "Tickets " @tickets-sold)

    ;; Shutdown running agents
    (shutdown-agents)
    )

  ;; MATH 

  (println (+ 1 2 3)) ;; Add values together
  (println(- 5 3 2)) ;; Subtract values
  (println(* 2 5)) ;; Multiply Values
  (println(/ 10 5)) ;; Divide Values
  (println(mod 12 5)) ;; Modulus
  (println(inc 5)) ;; Increment
  (println(dec 5)) ;; Decrement

  (println(Math/abs -10)) ;; Absolute Value
  (println(Math/cbrt 8)) ;; Cube Root
  (println(Math/sqrt 4)) ;; Square Root
  (println(Math/ceil 4.5)) ;; Round up
  (println(Math/floor 4.5)) ;; Round down
  (println(Math/exp 1)) ;; e to the power of 1
  (println(Math/hypot 2 2)) ;; sqrt(x^2 + y^2)
  (println(Math/log 2.71828)) ;; Natural logarithm
  (println(Math/log10 100)) ;; Base 10 log
  (println(Math/max 1 5))
  (println(Math/min 1 5))
  (println(Math/pow 2 2)) ;; Power

  ;; Generate random number
  (println (rand-int 20))

  ;; cos, sin, tan acos, asin, atan, cosh, sinh, tanh

  ;; Perform an operation on a collection
  (reduce + [1 2 3])
  (reduce - [1 2 3])

  (Math/PI)

  ;; FUNCTIONS
  ;; Define a function with 1 parameter named name

  (defn say-hello
    "Receives a name and responds with Hello Again name"

    ;; Attributes for the function
    [name]

    ;; Output the text and value
    (println "Hello Again"  name))

  (defn get-sum
    [x y]

    ;; The output from the last operation is returned
    (+ x y))

  ;; You can receive an unknown number of parameters
  (defn get-sum-more
    ([x y z]
    (+ x y z))

    ([x y]
    (+ x y)))

  ;; Receive a variable number of parameters in a list
  (defn hello-you
    [name]
    ;; Another way to combine strings
    (str "Hello " name))

  (defn hello-all
    [& names]

    ;; Pass values to hello-you
    (map hello-you names))

  ;; DECISION MAKING

  ;; RELATIONAL OPERATORS
  ;; = not= < <= > >=
  (= 4 5)
  (not= 4 5)

  ;; LOGICAL OPERATORS
  ;; and or not
  (and true false)
  (or true false)
  (not true)

  ;; IF THEN ELSE

  (defn can-vote
    [age]

    ;; If the statement is true execute the 1st, or 2nd if false
    (if (>= age 18)
      (println "You can Vote")
      (println "You can't Vote")))

  (defn can-do-more
    [age]

    ;; You can perform multiple actions with do
    (if (>= age 18)
      (do (println "You can Drive")
          (println "You can Vote"))
      (println "You can't Vote")))

  ;; WHEN
  ;; Is used when you want to do many things if true

  (defn when-ex
    [tof]

    (when tof
      (println "1st Thing")
      (println "2nd Thing")))

  ;; COND
  ;; Check for multiple conditions
  (defn what-grade
    [n]
    (cond
      (< n 5) "Preschool"
      (= n 5) "Kindergarten"
      (and (> n 5) (<= n 18)) (format "Go to Grade %d" (- n 5))
      :else "Go to College"))

  ;; LOOPING
  ;; WHILE LOOPS
  ;; Loop while condition is true

  (defn one-to-x
    [x]

    ;; Value that increments
    (def i (atom 1))

    ;; Loop while true
    (while (<= @i x)
      (do
        (println @i)

        ;; Increment value
        (swap! i inc))))

  ;; DOTIMES LOOP
  ;; Execute a statement a set number of times

  (defn dbl-to-x
    [x]

    ;; i is incremented each time through
    (dotimes [i x]
      (println (* i 2))))

  ;; LOOP LOOP
  ;; Loop through values using recur to change a value
  ;; until a condition is no longer true

  (defn triple-to-x
    [x y]

    ;; Set starting value of i
    (loop [i x]

      ;; Cycle while true
      (when (< i y)
        (println (* i 3))

        ;; Increment the value
        (recur (+ i 1)))))

  ;; DOSEQ LOOP
  ;; Iterates through a sequence
  (defn print-list

    ;; Holds list passed
    [& nums]

    ;; As you cycle through the list store each item in x
    (doseq [x nums]
      (println x)))

  ;; FILE I/O

  (use 'clojure.java.io)

  (defn write-to-file
    [file text]

    ;; with-open opens and closes the file
    ;; and then writes a string to a file
    (with-open [wrtr (writer file)]
      (.write wrtr text)))

  (defn read-from-file
    [file]

    ;; We can catch a potential file not found error
    ;; with exception handling

    (try
      ;; Read from a file to a single string
      (println (slurp file))

      ;; Catch the error and print it
      (catch Exception e (println "Error : " (.getMessage e)))))

  ;; Append text to a file
  (defn append-to-file
    [file text]

    (with-open [wrtr (writer file :append true)]
      (.write wrtr text)))

  ;; Read 1 line at a time
  (defn read-line-from-file
    [file]

    (with-open [rdr (reader file)]
      (doseq [line (line-seq rdr)]
        (println line))))

  ;; DESTRUCTURING
  ;; Binding of values in a data structure to symbols

  (defn destruct
    []
    (def vectVals [1 2 3 4])

    ;; Assign values to symbols
    ;; the-rest stores remaining values
    (let [[one two & the-rest] vectVals]
    (println one two the-rest)))

  ;; STRUCTMAPS
  ;; Used to define a complex custom type

  (defn struct-map-ex
    []

    ;; Define a Struct
    (defstruct Customer :Name :Phone)

    ;; Define a Struct Object
    (def cust1 (struct Customer "Doug" 4125551212))

    ;; You can also assign to specific keys
    (def cust2 (struct-map Customer :Name "Sally" :Phone 5551122))

    (println cust1)

    ;; Access individual fields
    (println (:Name cust2))
    )

  ;; ADVANCED FUNCTIONS

  ;; Anonymous Functions
  ;; Function with no name

  ;; Create a list by multiplying all values by themselves
  (map (fn [x] (* x x)) (range 1 10))

  ;; Compact anonymous function multiplies everything by 3
  (map #(* % 3) (range 1 10))

  ;; Compact anon with 2 arguments
  (#(* %1 %2) 2 3)

  ;; CLOJURES
  ;; Return a custom function
  ;; Run in Repl
  ;; (defn custom-multiplier
  ;;  [mult-by]
  ;;  #(* % mult-by))

  ;; (def mult-by-3 (custom-multiplier 3))
  ;; (mult-by-3 3)

  ;; Where your code starts execution
  (defn -main
    "I don't do a whole lot ... yet."
    [& args]

    ;; FUNCTIONS
    ;; Call for the function to execute

    (say-hello "Derek")
    (get-sum 4 5)
    (get-sum-more 1 2 3)
    (hello-all "Doug" "Mary" "Paul")
    (println "Mult by 3")

    ;; DECISION MAKING
    (can-vote 17)
    (can-do-more 24)
    (when-ex true)
    (what-grade 19)

    ;; ATOMS
    (atom-ex 5)

    ;; LOOPING
    (one-to-x 5)
    (dbl-to-x 5)
    (triple-to-x 1 5)
    (print-list 7 8 9)

    ;; FILE I/O
    (write-to-file "test.txt" "This is a sentence\n")
    (read-from-file "test.txt")
    (append-to-file "test.txt" "This is another sentence\n")
    (read-line-from-file "test.txt")

    ;; DESTRUCTURING
    (destruct)

    ;; STRUCTMAPS
    (struct-map-ex)

    ;; AGENTS
    (agent-ex)

    ;; TAKE DROP
    (take-drop-ex)
  )
  (ns tut2.core
    (:gen-class))

  (defn take-drop
    []

    ;; FILTERING LISTS
    ;; TAKE DROP TAKE-WHILE DROP-WHILE FILTER
    ;; Remove 1st 2
    (println (take 2 [1 2 3]))

    ;; Remove after the 1st
    (println (drop 1 [1 2 3]))

    ;; Take what matches a condition
    (println (take-while neg? [-1 0 1]))

    ;; Drop what matches a condition
    (println (drop-while neg? [-1 0 1]))

    ;; Return what matches
    (println (filter #(> % 2) [1 2 3 4]))

    (println (rand) 0.5)

    )

  ;; MACROS
  ;; Macros generate code when you need to define when
  ;; or if arguments should be evaluated

  ;; This macro will print different discounts based on
  ;; if the person is over 65 or not
  (defmacro discount
    ([cond dis1 dis2]

     ;; Syntax Quoting tells clojure not to evaluate if, but
     ;; to just return it
     (list `if cond dis1 dis2)))

  ;; Create (+ 2 5) when passed (2 + 5)
  (defmacro reg-math
    [calc]

    (list (second calc) (first calc) (nth calc 2)))

  ;; Execute multiple statements with do
  (defmacro do-more
    [cond & body]

    ;; If condition is true combine and return all past
    ;; statements in a list for execution
    (list `if cond (cons 'do body)))

  (defmacro do-more-2
    [cond & body]

    ;; You can surround everything with syntax quoting and
    ;; then unquote single values with ~ and multiples with
    ;; ~@
    `(if ~cond (do ~@body)))

  (defn -main
    "I don't do a whole lot ... yet."
    [& args]
    (take-drop)

    ;; MACROS
    (discount (> 25 65) (println "10% off") (println "Full Price"))

    (reg-math (2 + 5))

    ;; macroexpand tells us what the macro does
    (macroexpand `(reg-math (2 + 5)))

    (do-more (< 1 2) (println "Hello") (println "Hello Again"))

    (do-more-2 (< 1 2) (println "Hello") (println "Hello Again"))

    )

  ```
-

## Source Pointers

- `raw/sources/Clojure.md`
