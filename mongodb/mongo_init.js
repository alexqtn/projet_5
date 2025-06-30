// 1. Utiliser la base 'admin' pour créer les rôles et utilisateurs principaux
db = db.getSiblingDB("admin");  // On se place sur la base admin

// 2. Créer un rôle admin personnalisé en héritant des rôles MongoDB standards
db.createRole({
  role: "admin_role",  // Nom du rôle personnalisé
  privileges: [],      // Pas d'actions personnalisées ici
  roles: [             // Héritage des rôles MongoDB intégrés
    { role: "userAdminAnyDatabase", db: "admin" },     // Gérer les utilisateurs
    { role: "dbAdminAnyDatabase", db: "admin" },       // Tâches d'administration des BDD
    { role: "readWriteAnyDatabase", db: "admin" },     // Lecture/écriture sur toutes les BDD
    { role: "clusterAdmin", db: "admin" }              // Gestion du serveur/cluster
  ]
});

// 3. Créer l’utilisateur admin principal avec ce rôle
db.createUser({
  user: "admin_user",                           // Nom d'utilisateur
  pwd: "admin123",                             // Mot de passe (à changer en prod)
  roles: [{ role: "admin_role", db: "admin" }]  // Rôle attribué
});


// 4. Passer à la base de données applicative principale
db = db.getSiblingDB("healthcare_db");  // On se place sur la base utilisée par l’application

// 5. Créer un rôle ingénieur avec accès lecture/écriture + gestion des collections
db.createRole({
  role: "engineer_role",  // Nom du rôle
  privileges: [
    {
      resource: { db: "healthcare_db", collection: "" },  // Toutes les collections de cette DB
      actions: [
        "find",              // Lire les documents
        "insert",            // Insérer des documents
        "update",            // Mettre à jour des documents
        "remove",            // Supprimer des documents
        "createCollection",  // Créer des collections
        "createIndex"        // Créer des index
      ]
    }
  ],
  roles: []  // Aucun rôle hérité
});

// 6. Créer un rôle analyste en lecture seule
db.createRole({
  role: "analyst_role",  // Nom du rôle
  privileges: [
    {
      resource: { db: "healthcare_db", collection: "" },  // Toutes les collections de cette DB
      actions: [
        "find",              // Lire les documents
        "listIndexes",       // Voir les index
        "listCollections"    // Lister les collections
      ]
    }
  ],
  roles: []  // Aucun rôle hérité
});

// 7. Créer l’utilisateur ingénieur avec le rôle associé
db.createUser({
  user: "engineer_user",                            // Nom d’utilisateur
  pwd: "engineer123",                               // Mot de passe
  roles: [{ role: "engineer_role", db: "healthcare_db" }]  // Rôle attribué
});

// 8. Créer l’utilisateur analyste avec accès lecture seule
db.createUser({
  user: "analyst_user",                             // Nom d’utilisateur
  pwd: "analyst123",                                // Mot de passe
  roles: [{ role: "analyst_role", db: "healthcare_db" }]  // Rôle attribué
});