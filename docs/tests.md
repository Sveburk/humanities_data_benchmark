# Test Overview

This page provides an overview of all tests. Click on the test name to see the detailed results.

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
    <th>Test</th>
    <th>Name</th>
    <th>Provider</th>
    <th>Model</th>
    <th>Dataclass</th>
    <th>Temperature</th>
    <th>Role Description</th>
    <th>Prompt File</th>
    <th>Legacy Test</th>

  </tr></thead>
  <tbody>
<tr>
    <td><a href='tests/T01'><span class='test-square' style='background-color: #99ccff;'>T01</span></a></td>
    <td><a href="/benchmarks/test_benchmark/">test_benchmark</a></td>
    <td><span class='test-rectangle' style='background-color: #ff0066;'>openai</span></td>
    <td><span class='test-rectangle' style='background-color: #33ccff;'>gpt-4o</span></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T02'><span class='test-square' style='background-color: #0099ff;'>T02</span></a></td>
    <td><a href="/benchmarks/test_benchmark/">test_benchmark</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #f39c12;'>gemini-2.0-flash</span></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T03'><span class='test-square' style='background-color: #33ccff;'>T03</span></a></td>
    <td><a href="/benchmarks/test_benchmark/">test_benchmark</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #cc6699;'>claude-3-5-sonnet-20241022</span></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T04'><span class='test-square' style='background-color: #ff3300;'>T04</span></a></td>
    <td><a href="/benchmarks/test_benchmark2/">test_benchmark2</a></td>
    <td><span class='test-rectangle' style='background-color: #ff0066;'>openai</span></td>
    <td><span class='test-rectangle' style='background-color: #33ccff;'>gpt-4o</span></td>
    <td></td>
    <td>0.5</td>
    <td>You are a Historian</td>
    <td>a_prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T05'><span class='test-square' style='background-color: #2c3e50;'>T05</span></a></td>
    <td><a href="/benchmarks/test_benchmark2/">test_benchmark2</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #f39c12;'>gemini-2.0-flash</span></td>
    <td></td>
    <td>0.5</td>
    <td>You are a Historian</td>
    <td>a_prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T06'><span class='test-square' style='background-color: #33ccff;'>T06</span></a></td>
    <td><a href="/benchmarks/test_benchmark2/">test_benchmark2</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #cc6699;'>claude-3-5-sonnet-20241022</span></td>
    <td></td>
    <td>0.5</td>
    <td>You are a Historian</td>
    <td>a_prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T07'><span class='test-square' style='background-color: #ff99cc;'>T07</span></a></td>
    <td><a href="/benchmarks/bibliographic_data/">bibliographic_data</a></td>
    <td><span class='test-rectangle' style='background-color: #ff0066;'>openai</span></td>
    <td><span class='test-rectangle' style='background-color: #33ccff;'>gpt-4o</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a Historian</td>
    <td></td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T08'><span class='test-square' style='background-color: #ffcc33;'>T08</span></a></td>
    <td><a href="/benchmarks/bibliographic_data/">bibliographic_data</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #f39c12;'>gemini-2.0-flash</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a Historian</td>
    <td></td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T09'><span class='test-square' style='background-color: #ff0066;'>T09</span></a></td>
    <td><a href="/benchmarks/bibliographic_data/">bibliographic_data</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #cc6699;'>claude-3-5-sonnet-20241022</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a Historian</td>
    <td></td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T10'><span class='test-square' style='background-color: #ff6600;'>T10</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff0066;'>openai</span></td>
    <td><span class='test-rectangle' style='background-color: #33ccff;'>gpt-4o</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T11'><span class='test-square' style='background-color: #ff6600;'>T11</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff0066;'>openai</span></td>
    <td><span class='test-rectangle' style='background-color: #9b59b6;'>gpt-4.5-preview</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T12'><span class='test-square' style='background-color: #6633ff;'>T12</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff0066;'>openai</span></td>
    <td><span class='test-rectangle' style='background-color: #34495e;'>gpt-4o-mini</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T13'><span class='test-square' style='background-color: #ff6600;'>T13</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #f39c12;'>gemini-2.0-flash</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T14'><span class='test-square' style='background-color: #34495e;'>T14</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #9b59b6;'>gemini-exp-1206</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T15'><span class='test-square' style='background-color: #ff0099;'>T15</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #2ecc71;'>gemini-1.5-flash</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T16'><span class='test-square' style='background-color: #33ffcc;'>T16</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #3399ff;'>gemini-1.5-pro</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T17'><span class='test-square' style='background-color: #9b59b6;'>T17</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #f1c40f;'>claude-3-7-sonnet-20250219</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T18'><span class='test-square' style='background-color: #99ff33;'>T18</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #cc6699;'>claude-3-5-sonnet-20241022</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T19'><span class='test-square' style='background-color: #0099ff;'>T19</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #e74c3c;'>gemini-2.5-pro-exp-03-25</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T20'><span class='test-square' style='background-color: #ff5050;'>T20</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #ff0033;'>gemini-2.0-flash-lite</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T21'><span class='test-square' style='background-color: #9933ff;'>T21</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #7f8c8d;'>gemini-2.0-pro-exp-02-05</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T22'><span class='test-square' style='background-color: #2980b9;'>T22</span></a></td>
    <td><a href="/benchmarks/fraktur/">fraktur</a></td>
    <td><span class='test-rectangle' style='background-color: #ffcc33;'>genai</span></td>
    <td><span class='test-rectangle' style='background-color: #e74c3c;'>gemini-2.5-pro-exp-03-25</span></td>
    <td></td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T23'><span class='test-square' style='background-color: #ff0066;'>T23</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #f1c40f;'>mistral</span></td>
    <td><span class='test-rectangle' style='background-color: #34495e;'>pixtral-large-latest</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history. You only return valid JSON an no other text.</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T24'><span class='test-square' style='background-color: #e74c3c;'>T24</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #f1c40f;'>claude-3-7-sonnet-20250219</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
</tr>
<tr>
    <td><a href='tests/T25'><span class='test-square' style='background-color: #ff6600;'>T25</span></a></td>
    <td><a href="/benchmarks/metadata_extraction/">metadata_extraction</a></td>
    <td><span class='test-rectangle' style='background-color: #ff5050;'>anthropic</span></td>
    <td><span class='test-rectangle' style='background-color: #f1c40f;'>claude-3-7-sonnet-20250219</span></td>
    <td>Document</td>
    <td>0.0</td>
    <td>You are a historian with keyword knowledge and an expert in the field of 20th century Swiss history</td>
    <td>prompt.txt</td>
    <td>false</td>
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
