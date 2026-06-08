use LMS_Database;

// =========================
// STUDENT PERFORMANCE
// =========================
db.enrollments.aggregate([
  {
    $group: {
      _id: "$student_id",
      total_courses: { $sum: 1 },
      average_progress: { $avg: "$progress_percentage" },
      completed_courses: {
        $sum: { $cond: [{ $eq: ["$status", "Completed"] }, 1, 0] }
      },
      dropped_courses: {
        $sum: { $cond: [{ $eq: ["$status", "Dropped"] }, 1, 0] }
      }
    }
  },
  { $out: "analytics_student_performance" }
]);

// =========================
// COURSE ENGAGEMENT
// =========================
db.enrollments.aggregate([
  {
    $group: {
      _id: "$course_id",
      total_students: { $sum: 1 },
      average_progress: { $avg: "$progress_percentage" },
      active_students: {
        $sum: { $cond: [{ $eq: ["$status", "Active"] }, 1, 0] }
      },
      completed_students: {
        $sum: { $cond: [{ $eq: ["$status", "Completed"] }, 1, 0] }
      },
      dropped_students: {
        $sum: { $cond: [{ $eq: ["$status", "Dropped"] }, 1, 0] }
      }
    }
  },
  { $out: "analytics_course_engagement" }
]);

// =========================
// AT-RISK STUDENTS
// =========================
db.enrollments.aggregate([
  {
    $match: {
      $or: [
        { progress_percentage: { $lt: 40 } },
        { status: "Dropped" }
      ]
    }
  },
  {
    $project: {
      student_id: 1,
      course_id: 1,
      progress_percentage: 1,
      status: 1,
      risk_reason: {
        $cond: [
          { $eq: ["$status", "Dropped"] },
          "Dropped course",
          "Low progress"
        ]
      }
    }
  },
  { $out: "analytics_at_risk_students" }
]);
