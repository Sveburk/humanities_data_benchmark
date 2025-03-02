
# Humanities Data Benchmark
Welcome to the **Humanities Data Benchmark** report page. This page provides an overview of all benchmark tests, 
results, and comparisons.

## Latest Benchmark Results

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script><style>
    /* Square styles */
    .test-rectangle {
        display: inline-block;
        height: 20px;
        border-radius: 3px;
        text-align: center;
        line-height: 20px;
        font-size: 10px;
        font-weight: regular;
        color: white;
        padding: 0 5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .test-square {
        display: inline-block;
        width: 30px;
        height: 20px;
        border-radius: 3px;
        text-align: center;
        line-height: 20px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
</style>
<table id="data-table" class="display">
  <thead><tr>
    <th>Benchmark</th>
    <th>Latest Results</th>

  </tr></thead>
  <tbody>
<tr>
    <td>test_benchmark</td>
    <td><a href='archive/2025-03-01/T01'><span class='test-square' style='background-color: #99ccff;'>T01</span></a>: 2025-03-01 <img src="https://img.shields.io/badge/score-niy-brightgreen" alt="score"><br><a href='archive/2025-03-01/T02'><span class='test-square' style='background-color: #0099ff;'>T02</span></a>: 2025-03-01 <img src="https://img.shields.io/badge/score-niy-brightgreen" alt="score"><br><a href='archive/2025-03-01/T03'><span class='test-square' style='background-color: #33ccff;'>T03</span></a>: 2025-03-01 <img src="https://img.shields.io/badge/score-niy-brightgreen" alt="score"><br></td>
</tr>
<tr>
    <td>test_benchmark2</td>
    <td><a href='archive/2025-03-01/T04'><span class='test-square' style='background-color: #ff3300;'>T04</span></a>: 2025-03-01 <img src="https://img.shields.io/badge/score-niy-brightgreen" alt="score"><br><a href='archive/2025-03-01/T05'><span class='test-square' style='background-color: #2c3e50;'>T05</span></a>: 2025-03-01 <img src="https://img.shields.io/badge/score-niy-brightgreen" alt="score"><br><a href='archive/2025-03-02/T06'><span class='test-square' style='background-color: #33ccff;'>T06</span></a>: 2025-03-02 <img src="https://img.shields.io/badge/score-niy-brightgreen" alt="score"><br></td>
</tr>
<tr>
    <td>bibliographic_data</td>
    <td><a href='archive/2025-03-02/T07'><span class='test-square' style='background-color: #ff99cc;'>T07</span></a>: 2025-03-02 <img src="https://img.shields.io/badge/fuzzy-0.6102080673748401-brightgreen" alt="fuzzy"><br><a href='archive/2025-03-02/T08'><span class='test-square' style='background-color: #ffcc33;'>T08</span></a>: 2025-03-02 <img src="https://img.shields.io/badge/fuzzy-0.0-brightgreen" alt="fuzzy"><br><a href='archive/2025-03-02/T09'><span class='test-square' style='background-color: #ff0066;'>T09</span></a>: 2025-03-02 <img src="https://img.shields.io/badge/fuzzy-0.0-brightgreen" alt="fuzzy"><br></td>
</tr>
<tr>
    <td>metadata_extraction</td>
    <td><span class='test-square' style='background-color: #ff6600;'>T10</span>: No results available<br></td>
</tr>

  </tbody>
</table>

<script>
  $(document).ready(function() {
    $('#data-table').DataTable({
      "paging": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "lengthMenu": [[10, 20, -1], [10, 20, "All"]],
    });
  });
</script>



## About This Page
This benchmark suite is designed to test **AI models** on humanities data tasks. The tests run **weekly** and 
results are automatically updated.

For more details, visit the [GitHub repository](https://github.com/RISE-UNIBAS/humanities_data_benchmark).