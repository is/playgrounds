(defproject us.yuxin.demo/chdbits2 "1.0.0-SNAPSHOT"
  :description "Automatic torrents downloader from CHDBits."
  :url "https://github.com/is/demos/tree/master/chdbits2"
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [clj-http "0.7.2"]
                 [com.typesafe/config "1.0.0"]]
  :plugins [[lein-pprint "1.1.1"]
    [lein-idea "1.0.1"]]
  :min-lein-version "2.0.0"
  :repositories [
    ["is-release" "http://scm4i:8081/artifactory/is-release"]
    ["is-snapshot" {
      :url "http://scm4i:8081/artifactory/is-snapshot"
      :snapshots true
      :update :always
      }]
    ]
  ;:mirrors {
  ;  "central" {:name "is-release" :url "http://scm4i:8081/artifactory/is-release" :username "is" :password :env}
  ;  "clojars" {:name "is-release" :url "http://scm4i:8081/artifactory/is-release" :username "is" :password :env}
  ; }
  :plugin-repositories [["plugins-release" "http://scm4i:8081/artifactory/plugins-release"]]
  :local-repo "local-m2"
  :javac-options ["-target" "1.7" "-source" "1.7" "-Xlint:-options"]
  :omit-source true
  :source-paths ["src" "src/main/clojure"]
  :java-source-paths ["src/main/java"]
  :compile-path "target/classes"
  :target-path "target"
  )
