(ns cw-practice)

(defn largest-diff [lst]
  "take a list a returnt the longest list fromt he head to the last >= elem"
  (reduce (fn [acc elem]
            (if
                (>= elem (:target acc)) (reduced acc)
                (merge acc {:list (rest (:list acc))})))
          {:list lst :target (first lst)} lst)) 

(largest-diff [1 2 3 4 1])
