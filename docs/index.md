
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


defaultdict(<class 'list'>, {'test_benchmark': ['T01', 'T02', 'T03'], 'test_benchmark2': ['T04', 'T05', 'T06'], 'bibliographic_data': ['T07', 'T08', 'T09'], 'metadata_extraction': ['T10']})

{}


## About This Page
This benchmark suite is designed to test **AI models** on humanities data tasks. The tests run **weekly** and 
results are automatically updated.

For more details, visit the [GitHub repository](https://github.com/RISE-UNIBAS/humanities_data_benchmark).