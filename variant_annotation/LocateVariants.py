import os
from sbgsdk import Process, define
from sbgsdk.file_utils import insert_suffix


class LocateVariants(define.Wrapper):
    Meta = dict(
        name = "Variant Annotation",
        description = "Using bioc variant annotation and analysis packages to explore our varaints data",
        version = "0.1.0",
        categories = "",
        toolkit = "",
        toolkit_version = "",
        licenses = ['GPLv3'],
        resources = dict(memory_gb=4, cpu='LOW', io='HIGH')
        )

    class Inputs(define.Inputs):
        inp_gz = define.input(
            name = "bgziped vcf",
            description = "bgziped vcf file with .gz extension",
##            file_types = "archive",
            required = True,
            list = False
            )

    class Outputs(define.Outputs):
        table = define.output(
            name = "variant summary table",
            description = "summary counts for given genomics features",
            file_types = "text",
            list = True
            )

    class Params(define.Params):
        genome = define.enum(
            values = [('hg19','hg19'),
                      ('hg18', 'hg18')],
            name = "reference genome",
            description = "choose reference genome, now we only support hg18, hg19",
            default = "hg19",
            category = "Reference Options"
            )
        location = define.enum(
            values = [
                ('all', 'including coding, 3 and 5 UTR, intron, integenic, spliceSite and promoter'),
                ('coding',  'falls within a coding region'),
                ('fiveUTR', 'falls within a 5 untranslated region'),
                ('threeUTR', 'falls within a 3 untranslated region'),
                ('intron', 'falls within an intron region'),
                ('intergenic', 'does not fall within a transcript associated with a gene'),
                ('splicSite', 'overlaps any portion of the first 2 or last 2 nucleotides of an intron'),
                ('promoter',  'falls within a promoter region of a transcript')
             ],
             name = "Location",
             description = "Choose locations you want to compute summary",
             default = "all",
             category = "Location options"
            )

        upstream = define.integer(
            name = "upstream",
            description = "Integer value to specify upstream of given category, promoter or intergenic region",
            default = 0,
            category = "Location extestion options"
            )

        downstream = define.integer(
            name = "downstream",
            description = "Integer value to specify downstream of given category, promoter or intergenic region",
            default = 0,
            category = "Location extestion options"
            )

    def execute(self):
        inputs, outputs, params = self.inputs, self.outputs, self.params

        output_dir = "locateVariant"


        ## outputs
        out_dir = 'locate_variant_summary'
        os.makedirs(out_dir)

        table = outputs.table
        table.file =  out_dir + 'table.txt'
        ## table.meta = inputs.sam.make_metadata(file_type='text')


        ## command line
        proc = Process("Rscript", stdout = table.file)
        proc.add_arg('--default-packages=VariantAnnotation')
        proc.add_arg('--vanilla')
        script_path = '/sbgenomics/variant_annotation/locateVariants.R'
        proc.add_arg(script_path)
        proc.add_arg(inputs.inp_gz)
        proc.add_arg(params.genome)
        proc.add_arg(params.location)
        proc.add_arg(out_dir)

        proc.run()



def test_locate_variants():
    inputs, params = {'inp_gz': '/sbgenomics/test-data/chr22.vcf.gz'}, {}
    outputs = LocateVariants(inputs, params).test()
