`include "defines.v"

module mode1_max(
  inp0,
  inp1,
  inp2,
  inp3,
  
  ex_inp,
  
  outp); 
  
  input  [`DATAWIDTH-1 : 0] inp0;
  input  [`DATAWIDTH-1 : 0] inp1;
  input  [`DATAWIDTH-1 : 0] inp2;
  input  [`DATAWIDTH-1 : 0] inp3;

  input  [`DATAWIDTH-1 : 0] ex_inp;

  output [`DATAWIDTH-1 : 0] outp;

  wire   [`DATAWIDTH-1 : 0] cmp0_out;
  wire   [`DATAWIDTH-1 : 0] cmp1_out;
  wire   [`DATAWIDTH-1 : 0] cmp2_out;

  DW_fp_cmp #(`MANTISSA, `EXPONENT, `IEEE_COMPLIANCE) cmp0(.a(inp0),       .b(inp1),     .z1(cmp0_out), .zctr(1'b0), .aeqb(), .altb(), .agtb(), .unordered(), .z0(), .status0(), .status1());
  DW_fp_cmp #(`MANTISSA, `EXPONENT, `IEEE_COMPLIANCE) cmp1(.a(inp2),       .b(inp3),     .z1(cmp1_out), .zctr(1'b0), .aeqb(), .altb(), .agtb(), .unordered(), .z0(), .status0(), .status1());
  DW_fp_cmp #(`MANTISSA, `EXPONENT, `IEEE_COMPLIANCE) cmp2(.a(cmp0_out),   .b(cmp1_out), .z1(cmp2_out), .zctr(1'b0), .aeqb(), .altb(), .agtb(), .unordered(), .z0(), .status0(), .status1());
   
  DW_fp_cmp #(`MANTISSA, `EXPONENT, `IEEE_COMPLIANCE) ex_cmp(.a(cmp2_out), .b(ex_inp),   .z1(outp),     .zctr(1'b0), .aeqb(), .altb(), .agtb(), .unordered(), .z0(), .status0(), .status1());
endmodule

