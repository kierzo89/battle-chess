/* Diagnostic recording callbacks, explicitly not the original hardware callees.
   The execution harness never calls initialize_io/write_bytes/read_bytes. */
unsigned serial_diagnostic_calls,serial_diagnostic_format,serial_diagnostic_byte;
void far restore_mode_10e0d(void) { ++serial_diagnostic_calls; }
void far set_serial_format_10d3_0000(unsigned value)
{
    ++serial_diagnostic_calls;
    serial_diagnostic_format=value;
}
void far enable_serial_irq_10d3_0023(void) { ++serial_diagnostic_calls; }
void far write_byte_far(unsigned value)
{
    ++serial_diagnostic_calls;
    serial_diagnostic_byte=value;
}
