(ns chdbits2.core
  (:require [clj-http.client :as client]
            [crouton.html :as html])
  (:import
    (java.io File)
    (com.typesafe.config Config ConfigFactory)))

(declare main)

(def ^Config config (ConfigFactory/parseFile (File. "application.json")))

(defn- stream [^String s]
  (java.io.ByteArrayInputStream. (.getBytes s)))

(defn main
  [& args]
  (def body (:body (client/get "http://www.renren.com/")))
  (println (.getConfig config "chdbits"))
  (println (html/parse (stream body)))
  (println "hello world"))
