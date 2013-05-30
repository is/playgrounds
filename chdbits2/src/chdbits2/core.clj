(ns chdbits2.core
  (:import
    (java.io File)
    (com.typesafe.config Config ConfigFactory)))

(declare main)

(def ^Config config (ConfigFactory/parseFile (File. "application.json")))

(defn main
  [& args]
  (println (.getConfig config "chdbits"))
  (println "hello world"))

